import os
import logging
import time
import uuid
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from pyannote.audio import Pipeline
import torch
import torchaudio
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# FastAPI application
app = FastAPI()

# Logger configuration with emojis for better readability
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load Hugging Face API token from environment variable 🔐
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HUGGINGFACE_TOKEN:
    logger.error("❌ HUGGINGFACE_TOKEN environment variable is not set. Exiting...")
    raise RuntimeError("HUGGINGFACE_TOKEN environment variable is required.")

# Load the speaker diarization pipeline 🎙️
try:
    logger.info("🚀 Loading speaker diarization pipeline...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=HUGGINGFACE_TOKEN
    )
    logger.info("✅ Pipeline successfully loaded.")
except Exception as e:
    logger.error(f"❌ Failed to load the pipeline: {e}")
    raise RuntimeError("Failed to load the speaker diarization pipeline.")

# Check for GPU availability and move the pipeline accordingly 🔥
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipeline.to(device)
logger.info(f"🎛️ Pipeline running on: {device}")

# Pydantic model to validate the input URL
class AudioURL(BaseModel):
    url: HttpUrl  # Ensures the input is a valid URL

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """ Middleware to log all incoming requests with a unique ID. """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    logger.info(f"🆕 Request {request_id} received - {request.method} {request.url.path}")

    try:
        body = await request.json()
        logger.info(f"📩 Request body: {body}")
    except Exception:
        logger.info("⚠️ Unable to read request body.")

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(f"✅ Request {request_id} processed in {process_time:.4f} seconds - Status: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """ Global exception handler to catch and log unexpected errors. """
    request_id = getattr(request.state, "request_id", "UNKNOWN")
    logger.error(f"❌ Request {request_id} - Internal Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "request_id": request_id},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """ Exception handler for HTTP errors (e.g., bad requests, timeouts). """
    request_id = getattr(request.state, "request_id", "UNKNOWN")
    logger.warning(f"⚠️ Request {request_id} - HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "request_id": request_id},
    )

@app.post("/analyze")
async def analyze_audio(request: Request, audio_url: AudioURL):
    """
    Endpoint to analyze an audio file and perform speaker diarization.
    The input must be a publicly accessible MP3 URL.
    """
    request_id = getattr(request.state, "request_id", "UNKNOWN")
    logger.info(f"🎧 Request {request_id} - Downloading audio from {audio_url.url}")

    # Attempt to download the audio file
    try:
        response = requests.get(audio_url.url, timeout=10)
        response.raise_for_status()
        logger.info("✅ Audio file successfully downloaded.")
    except requests.Timeout:
        logger.error("⏳ Download request timed out.")
        raise HTTPException(status_code=408, detail="Download request timed out.")
    except requests.RequestException as e:
        logger.error(f"❌ Error downloading the audio file: {e}")
        raise HTTPException(status_code=400, detail=f"Error downloading the audio file: {e}")

    # Save the audio file temporarily
    with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
        temp_audio_file.write(response.content)
        temp_audio_path = temp_audio_file.name

    try:
        # Validate that the file is a readable audio file
        if not torchaudio.info(temp_audio_path):
            raise HTTPException(status_code=400, detail="Invalid or unreadable audio file.")

        # Load the audio using torchaudio
        waveform, sample_rate = torchaudio.load(temp_audio_path)
        logger.info(f"🔍 Audio loaded - Sample rate: {sample_rate}, Shape: {waveform.shape}")

        # Ensure the audio is long enough for diarization
        duration = waveform.shape[1] / sample_rate
        if duration < 1.0:
            raise HTTPException(status_code=400, detail="Audio file is too short for analysis.")

        # Perform speaker diarization
        diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

        # Format the results into a structured JSON response
        result = [
            {
                "speaker": label,
                "start": round(segment.start, 2),
                "end": round(segment.end, 2)
            }
            for segment, _, label in diarization.itertracks(yield_label=True)
        ]

        logger.info(f"✅ Request {request_id} - Analysis completed, {len(result)} segments detected.")

    except HTTPException as e:
        raise e  # Re-raise the exception if already handled
    except Exception as e:
        logger.error(f"❌ Error during audio analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Audio analysis error: {e}")
    finally:
        # Safely delete the temporary audio file after processing
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            logger.info(f"🗑️ Temporary file deleted.")

    return {"request_id": request_id, "segments": result}
