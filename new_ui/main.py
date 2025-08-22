from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import faiss
from sentence_transformers import SentenceTransformer
from helpers.generate_video import load_lecture_data, generate_video_answer

app = FastAPI()

# Mount the 'ui' directory to serve static files (HTML, CSS, JS)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Mount the 'data' directory for video assets
app.mount("/data", StaticFiles(directory="data"), name="data")

app.mount("/helpers", StaticFiles(directory="helpers"), name="helpers")

# Pydantic model for the incoming question data
class Question(BaseModel):
    question: str

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = faiss.read_index("data/sentence_embeddings.index")

lecture_sentences, lecture_data = load_lecture_data()

# Endpoint to serve the main HTML page
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())
    

# API endpoint to handle the question and return the video data
@app.post("/generate-video")
async def generate_video(question_data: Question):
    video_answer = generate_video_answer(question_data.question, model, faiss_index, lecture_sentences, lecture_data)
    return video_answer

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)