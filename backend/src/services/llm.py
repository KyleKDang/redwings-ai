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
    You are a friendly, encouraging snowboarding coach with deep biomechanics knowledge.
    Talk directly to the athlete like a real coach would — conversational, clear, and motivating.
    Avoid technical jargon where possible. Use plain language a snowboarder would understand.
    Be specific about what you saw in their video, not generic advice.
    Keep each point concise — 1-3 sentences max per item.
    Return ONLY valid JSON in the exact structure requested — no extra text or markdown.
    """

    user_payload = {
        "athlete_profile": profile,
        "biomechanical_metrics": metrics,
        "instructions": "Write like a real coach giving feedback after watching someone's video. Be encouraging but honest. Reference specific moments from the data (e.g. 'on your landings' or 'during the trick') rather than citing raw numbers.",
        "required_output_structure": {
            "overall_assessment": "2-3 sentences. Start with something positive, then the main thing to work on.",
            "form_corrections": [
                "Correction 1 — what you saw and how to fix it in plain language",
                "Correction 2",
                "Correction 3"
            ],
            "safety_warnings": [
                "Warning 1 — conversational, not clinical",
                "Warning 2"
            ],
            "drills": [
                "Drill 1 — name it, explain it simply, say why it helps",
                "Drill 2"
            ],
            "conditioning": "2-3 sentences on what to work on off the snow.",
            "motivation": "1 sentence of genuine encouragement specific to what they did well."
        }
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
