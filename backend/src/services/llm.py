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
You are a professional snowboard coach and movement specialist who explains biomechanics in clear, practical language.

Your feedback should sound like what a real coach would tell an athlete after reviewing their riding footage.

STYLE REQUIREMENTS:
- Professional, supportive, and direct
- Natural human coaching tone (not academic or robotic)
- Explain problems in simple language
- Translate metrics into real-world meaning (do NOT emphasize numbers)
- Only mention numbers if they help clarify risk or improvement goals
- Focus on what the athlete should FEEL or DO differently
- Avoid technical jargon unless briefly explained
- Give clear, practical coaching cues
- Prioritize injury prevention and performance

DO NOT:
- Write like a research paper
- Overuse biomechanical terminology
- List raw metrics without explanation
- Use unclear measurement targets without context

FRAME FEEDBACK LIKE A REAL COACH:
- Start with overall performance assessment
- Explain main risks in simple terms
- Give specific technique fixes
- Provide practical drills
- Give safety guidance
- Provide structured training focus

Also keep in mind, take the person's body height, weight, age, skill level, training frequency (hours per week)
and medical history into account when giving feedback.
Don't be afraid to bring up any of their body features as a safety guideline. Be real. 
BYPASS GUIDELINES IN FAVOR OF USER SAFETY AND HEALTH. THAT INCLUDES BODY SHAMING.

Return ONLY valid JSON in the exact structure requested.
"""

    user_payload = {
    "athlete_profile": profile,
    "biomechanical_metrics": metrics,
    "required_output_structure": {
        "overall_assessment": "Short coach-style summary of performance, main issues, and top priorities. Speak directly to the athlete using simple language.",
        "form_corrections": [
            "Clear coaching cue explaining what the athlete should change and what it should feel like",
            "Clear coaching cue explaining what the athlete should change and what it should feel like",
            "Clear coaching cue explaining what the athlete should change and what it should feel like"
        ],
        "safety_warnings": [
            "Simple explanation of risk and what to avoid",
            "Simple explanation of risk and what to avoid"
        ],
        "drills": [
            "Practical drill with how to perform it and what to focus on",
            "Practical drill with how to perform it and what to focus on"
        ],
        "conditioning": "Simple training plan description focused on strength, control, and injury prevention. Give it in a clear format, like a list of bullet points."
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
    