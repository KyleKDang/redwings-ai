import json
from openai import OpenAI
import json
import os
def generate_coaching_feedback(input_data: dict) -> dict:
    client = OpenAI(api_key=input_data["api_key"])

    profile = input_data["user_profile"]
    movement = input_data["movement"]
    metrics = input_data["metrics"]

    system_prompt = """
You are an elite Red Bull snowboarding performance coach with biomechanics expertise.
Analyze performance metrics and provide structured, safety-aware coaching feedback.
Be precise and practical.
Return ONLY valid JSON in the exact structure requested.
"""

    user_payload = {
        "movement": movement,
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
        reasoning_effort="low",
        verbosity="low"
    )

    content = response.choices[0].message.content

    # Safely parse JSON before returning
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON from model", "raw_response": content}