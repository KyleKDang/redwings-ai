from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# from services.pose import extract_metrics
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
    height_cm: float = Form(...),
    weight_kg: float = Form(...),
    fatigue_level: int = Form(...),
    injury_history: str = Form("None"),
):
    """
    Accepts a video upload + athlete profile form fields.
    Returns biomechanical metrics and AI coaching feedback.
    """
    # Validate video type
    if not video.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a video")

    # Read video bytes
    video_bytes = await video.read()

    # Step 1: Extract biomechanical metrics via MediaPipe
    # metrics = extract_metrics(video_bytes)
    metrics = None
    if "error" in metrics:
        raise HTTPException(status_code=422, detail=metrics["error"])

    # Step 2: Build profile dict
    profile = {
        "sport": sport,
        "skill_level": skill_level,
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "fatigue_level": fatigue_level,
        "injury_history": injury_history,
    }

    # Step 3: Generate coaching feedback via LLM
    coaching = generate_coaching_feedback(profile, metrics)

    return {
        "profile": profile,
        "metrics": metrics,
        "coaching": coaching,
    }
