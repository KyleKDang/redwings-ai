<<<<<<< HEAD
# Starter Pack Series: Full-Stack Web Application

A single-page React application backed by FastAPI, ready to deploy on Render or Vercel.

[Create a new repository using this template](https://github.com/new?template_name=starter-pack-full-stack-web-app&template_owner=HackAtUCI)
to get started.

## Introduction

Welcome to the starter-pack series on full-stack web applications! This
repository serves as an introduction to how full-stack web applications work
and how to leverage frameworks to make it easier to build one.

## What are Frontends and Backends?

A frontend is the software visible to a user such as what appears on a webpage,
while a backend is the software running behind the scenes such as an endpoint
providing the data that will eventually be shown on the webpage.

Frontends for webpages generally consist of HTML, CSS, and JavaScript that come
together to provide the user interface (UI) along with other visual assets.
While you can code directly in those languages, JavaScript libraries such as React
allow you to do the same faster and more efficiently.

Backends are much more flexible since all you need is a web server listening for
different types of [HTTP requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
on various routes (e.g. /user/info), each of which can perform its own action
such as modifying a database or triggering another action.
There are many libraries, such as FastAPI (Python) and Express (JavaScript) that make
it easy to build special servers known as APIs which interact with a frontend client.

## What is a Full-Stack Web App?

With the rising popularity of single-page applications (SPAs), simple webpages can be
made by keeping the frontend and backend in separate layers. This allows constructing
a full-stack web application with a frontend UI client and a backend API server.

For example, let's say you're trying to access a profile page on some website, and the
data is stored on a database somewhere. When the page loads, the client sends a request
to the server which, in turn, retrieves the corresponding data from the database.
The server then returns the data back to the client for the UI to display on the page.
This interaction is just one example of how a frontend and backend can work together to
provide a great and scalable experience for its users.

**Important:** You might be wondering why you couldn't just query the database directly
from the frontend. Databases require sensitive credentials for access, and if you store
those on the frontend, they _will_ be found no matter where you put them. Keeping them
on the server is much more secure because they won't be visible to the frontend.
This is relevant mainly for purely client-rendered applications: newer React frameworks
such as [Next.js](https://nextjs.org) promote a model of server rendering which unifies
the data fetching and rendering into one place for improved security and performance.

## This Application

This starter pack consists of a frontend UI made with [React](https://react.dev) and a
backend API made with [FastAPI](https://fastapi.tiangolo.com).

React is a JavaScript library for building composable and interactive components through
JSX which is markup similar to HTML. These components can be efficiently rendered to the
browser even as the data provided changes.

FastAPI is a Python framework for building APIs with simple functions and decorators.
The framework is easy to use and also, as the name implies, very fast.

For a deeper explanation on how the app is put together, please view the corresponding
`README` files for the [frontend](frontend/README.md) and [backend](backend/README.md).

For deploying this app to the internet, see [DEPLOYMENT.md](DEPLOYMENT.md).
=======
# RedWings AI

AI-powered injury prevention and performance coaching for extreme sports athletes. Upload a video of your trick or training run and get elite biomechanical analysis with personalized coaching advice — built at IrvineHacks 2026.

---

## What It Does

1. **Athlete Profile** — Enter your sport, skill level, body metrics, fatigue level, and injury history
2. **Video Upload** — Submit a video clip of your trick or training session
3. **Pose Detection** — MediaPipe extracts joint angles, symmetry, stance width, and movement velocity frame by frame
4. **AI Coaching** — GPT-5-mini turns the biomechanical data into actionable form corrections, safety warnings, drills, and a conditioning recommendation

---

## Tech Stack

**Frontend**
- React + Vite
- Tailwind CSS

**Backend**
- FastAPI
- MediaPipe Pose (computer vision)
- OpenCV
- OpenAI API (GPT-5-mini)

---

## Project Structure

```
redwings-ai/
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── ProfileForm.jsx
│       │   ├── VideoFeedback.jsx
│       │   └── Results.jsx
│       ├── App.jsx
│       ├── App.css
│       └── index.css
└── backend/
    ├── services/
    │   ├── media_pipe_processing.py
    │   ├── metrics.py
    │   └── llm.py
    ├── api.py
    ├── main.py
    ├── requirements.txt
    └── requirements-dev.txt
```

---

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- An OpenAI API key
- The MediaPipe `pose_landmarker_full.task` model file (place it in `backend/services/`)

You can download the model file here:
```
https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task
```

### Environment Setup

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

### Backend

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt
fastapi dev src/api.py
```

The API will be running at `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be running at `http://localhost:5173`. Vite proxies all `/api` requests to the FastAPI backend automatically.

---

## API

### `POST /api/analyze`

Accepts a video file and athlete profile, returns biomechanical metrics and AI coaching.

**Request** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `video` | file | Video file (.mp4, .mov, etc.) |
| `sport` | string | e.g. `"Snowboarding"` |
| `skill_level` | string | `"Beginner"`, `"Intermediate"`, `"Advanced"`, or `"Pro"` |
| `age` | int | Athlete age |
| `height_cm` | float | Height in centimeters |
| `weight_kg` | float | Weight in kilograms |
| `fatigue_level` | int | 1–10 scale |
| `injury_history` | string | Optional free text |

**Response**

```json
{
  "profile": { "sport": "Snowboarding", "skill_level": "Intermediate", "..." },
  "metrics": {
    "knee_angle_avg": 132.4,
    "knee_angle_min": 88.1,
    "knee_symmetry_avg": 12.3,
    "hip_angle_avg": 145.2,
    "arm_spread_avg": 0.38,
    "knee_velocity_max": 18.5
  },
  "coaching": {
    "form_corrections": ["...", "...", "..."],
    "safety_warnings": ["...", "..."],
    "drills": ["...", "..."],
    "conditioning": "...",
    "overall_assessment": "..."
  }
}
```

---

## Team

Built at IrvineHacks 2026 by a team of 4.
>>>>>>> 11f424673b60dccd82e44646a7a9dedbc95f5a7d
