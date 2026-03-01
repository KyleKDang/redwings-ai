import json
import os
from openai import OpenAI


def generate_coaching_feedback(profile: dict, metrics: dict) -> dict:
    """
    Takes athlete profile and biomechanical metrics from MediaPipe,
    returns structured coaching feedback as a dict.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)

    system_prompt = """
You are an elite extreme sports performance coach with biomechanics expertise.
Analyze the provided biomechanical metrics and athlete profile, then give structured,
actionable coaching feedback focused on injury prevention and technique improvement.
Be precise, practical, and safety-aware.
Return ONLY valid JSON in the exact structure requested — no extra text or markdown.
"""

    user_payload = {
        "athlete_profile": profile,
        "biomechanical_metrics": metrics,
        "required_output_structure": {
            "form_corrections": ["string", "string", "string"],
            "safety_warnings": ["string", "string"],
            "drills": ["string", "string"],
            "conditioning": "string",
            "overall_assessment": "string"
        }
    }

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, indent=2)}
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON from model", "raw_response": content}
    