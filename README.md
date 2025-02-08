# **FastDiarize 🎙️ – FastAPI Speaker Diarization API**  

🚀 **FastDiarize** is a lightweight and efficient **speaker diarization API** powered by **FastAPI** and **Pyannote.audio**. It enables **automatic speaker segmentation** in audio files using AI.  

✅ **Ultra-simple usage with Docker**  
✅ **GPU acceleration** when available  
✅ **Fully open-source & production-ready**  

---  

## **🔥 Quick Start with Docker (Recommended)**  

**1️⃣ Run the API in seconds with Docker:**  
```bash
docker run -d --gpus=all -p 8000:8000 -e HUGGINGFACE_TOKEN="your_huggingface_token" lumymedia/fastdiarize:latest
```
> ⚡ No installation needed! The API is instantly available at **http://localhost:8000**  


**2️⃣ Analyze an audio file**  
```bash
curl -X 'POST' 'http://localhost:8000/analyze' \
     -H 'Content-Type: application/json' \
     -d '{"url": "https://example.com/audio.mp3"}'
```
> 🎤 **FastDiarize** will return timestamps for each speaker  

---

## **📦 Manual Installation (Optional)**  

If you prefer to run the API manually:  

### **1️⃣ Clone the repository**  
```bash
git clone https://github.com/LumyDigitalAgency/FastDiarize.git
cd FastDiarize
```

### **2️⃣ Install dependencies**  
```bash
pip install -r requirements.txt
```

### **3️⃣ Set your Hugging Face API token**  
Create a `.env` file and add:  
```ini
HUGGINGFACE_TOKEN=your_huggingface_token
```

### **4️⃣ Run the API locally**  
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## **🐳 Deploy with Docker Compose**  

For a **fully managed deployment**, use **Docker Compose**:  

```bash
docker-compose up -d
```

---

## **🚀 API Endpoints**  

- **`POST /analyze`** – Analyze an audio file and detect speakers  


Example response from `POST /analyze`:  
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "segments": [
    {"speaker": "SPEAKER_1", "start": 0.00, "end": 3.50},
    {"speaker": "SPEAKER_2", "start": 3.51, "end": 7.80}
  ]
}
```

---

## **🎯 Contributing**  

Want to improve **FastDiarize**? Contributions are welcome!  

1️⃣ Fork the repo & create a new branch  
2️⃣ Make changes & commit  
3️⃣ Open a Pull Request  

---

## **📜 License**  

FastDiarize is released under the **MIT License**.  

⭐ **If you find this project useful, give it a star on GitHub!** 🚀