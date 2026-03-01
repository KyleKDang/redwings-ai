import os
import tempfile
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from services.media_pipe_processing import analyze_video
from services.metrics import extract_metrics
from services.llm import generate_coaching_feedback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
async def hello():
    return {"message": "RedWings AI backend is running"}


@app.post("/analyze")
async def analyze(
    video: UploadFile = File(...),
    sport: str = Form(...),
    skill_level: str = Form(...),
    age: int = Form(...),
    height_in: float = Form(...),
    weight_lbs: float = Form(...),
    training_hours: int = Form(...),
    injury_history: str = Form("None"),
    video_info: str = Form("None")
):
    # Validate video type
    if not video.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a video")

    # Write video bytes to a temp file so OpenCV can open it
    video_bytes = await video.read()
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    try:
        # Step 1: Run MediaPipe on the video to get raw joint data
        joint_data = analyze_video(tmp_path)

        if joint_data is None or len(joint_data) == 0:
            raise HTTPException(status_code=422, detail="No pose landmarks detected in video. Make sure the subject is clearly visible.")

        # Step 2: Extract biomechanical metrics from joint data
        metrics = extract_metrics(joint_data)

        if not metrics:
            raise HTTPException(status_code=422, detail="Could not extract metrics from video.")

    finally:
        os.unlink(tmp_path)

    # Step 3: Build profile dict
    profile = {
        "sport": sport,
        "skill_level": skill_level,
        "age": age,
        "height_in": round(height_in, 1),
        "weight_lbs": round(weight_lbs, 1),
        "training_hours": training_hours,
        "injury_history": injury_history,
        "video_info": video_info,
    }

    # Step 4: Generate coaching feedback via LLM
    # Pass a summary of metrics (not the full frame_by_frame) to keep the prompt concise
    metrics_summary = {k: v for k, v in metrics.items() if k not in ("frame_by_frame", "trick_phases")}
    coaching = generate_coaching_feedback(profile, metrics_summary)

    return {
        "profile": profile,
        "metrics": metrics_summary,
        "coaching": coaching,
    }