# FastDiarize 🎧 – FastAPI Speaker Diarization API

🚀 **FastDiarize** is a lightweight and efficient speaker diarization API powered by **FastAPI** and **Pyannote.audio**. It enables automatic speaker segmentation in audio files using AI.

---

## 🔥 Quick Start with Docker (Recommended)

### 1️⃣ Run the API in seconds with Docker (with GPU support):

```bash
docker run -d --gpus all -p 8000:8000 -e HUGGINGFACE_TOKEN="your_huggingface_token" lumymedia/fastdiarize:latest
```

💠 **No installation needed!** The API is instantly available at [http://localhost:8000](http://localhost:8000).

---

### 2️⃣ Analyze an audio file

Send a POST request to the `/analyze` endpoint with a publicly accessible MP3 URL:

```bash
curl -X 'POST' 'http://localhost:8000/analyze' \
     -H 'Content-Type: application/json' \
     -d '{"url": "https://example.com/audio.mp3"}'
```

---

### 3️⃣ Example API Response

The API returns timestamps for each speaker in the following format:

```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "segments": [
    {"speaker": "SPEAKER_1", "start": 0.00, "end": 3.50},
    {"speaker": "SPEAKER_2", "start": 3.51, "end": 7.80}
  ]
}
```

- **`request_id`**: A unique ID for the request.
- **`segments`**: A list of speaker segments with start and end times in seconds.

---

## 📝 Prerequisites

Before using FastDiarize, ensure you have the following:

- **Hugging Face API token**: Required to load the Pyannote.audio pipeline. [Get your token here](https://huggingface.co/settings/tokens).
- **Docker** (optional but recommended): For easy deployment.
- **Python 3.8+**: If running manually.

---

## ⚡ Notes & Considerations

FastDiarize is designed to be lightweight and easy to use, but here are a few things to keep in mind:

- The audio file must be **publicly accessible** via a URL.
- Currently, only **MP3 files** are supported.
- For best results, audio should be at least **1 second long**.
- Longer files may take more time to process.

Want to help improve these features? **Pull requests are welcome!** 🚀

---

## 🚀 Performance

- The API automatically uses **GPU acceleration** if available.
- Processing time depends on the **length of the audio file**.
- For optimal performance, ensure your system has a compatible GPU.

---

## ❓ Common Errors

Here are some common errors and how to resolve them:

- **408 Timeout**: The audio download took too long. Check the URL and try again.
- **400 Bad Request**: The audio file is invalid, too short, or inaccessible.
- **500 Internal Server Error**: An unexpected error occurred during analysis. Check the logs for details.

---

## 🛋️ Manual Installation (Optional)

If you prefer to run the API manually:

### 1️⃣ Clone the repository

```bash
git clone https://github.com/lumymedia/FastDiarize.git
cd FastDiarize
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set your Hugging Face API token

Create a `.env` file and add:

```plaintext
HUGGINGFACE_TOKEN=your_huggingface_token
```

### 4️⃣ Run the API locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🐳 Deploy with Docker Compose

For a fully managed deployment, use Docker Compose:

```bash
docker-compose up -d
```

---

## 🎯 Contributing

Want to improve **FastDiarize**? Contributions are welcome!

1️⃣ Fork the repo & create a new branch  
2️⃣ Make changes & commit  
3️⃣ Open a Pull Request  

---

## 🐟 License

**FastDiarize** is released under the **MIT License**.

🌟 If you find this project useful, give it a star on [GitHub](https://github.com/lumymedia/FastDiarize)! 🚀