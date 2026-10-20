import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Explicitly load backend/.env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

XAI_API_KEY = os.getenv("XAI_API_KEY")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-4-fast")

if not XAI_API_KEY:
    raise ValueError(
        "XAI_API_KEY was not found. Check that backend/.env exists "
        "and contains XAI_API_KEY."
    )

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)

SYSTEM_PROMPT = """You are an AI assistant for a municipal complaint intelligence system.
You will receive a citizen complaint as free text. Analyze it and respond with ONLY a valid JSON object
(no markdown, no explanation, no code fences) with exactly these keys:

- "category": one of "Water", "Electricity", "Roads", "Waste", "Other"
- "priority": one of "Low", "Medium", "High", "Critical"
- "location": the location mentioned in the complaint. If none is mentioned, use "Not specified"
- "duration": how long the issue has been happening, if mentioned. If none, use "Not specified"
- "problem_summary": a one-sentence plain-language summary of the actual problem
- "recommended_action": a concrete, specific action the municipal department should take

Base priority on urgency and safety risk described (e.g. sparking wires, flooding, sewage = Critical;
minor/cosmetic issues = Low). Be decisive - always pick exactly one category and one priority."""


def analyze_with_ai(complaint_text: str) -> dict:
    """
    Sends the complaint to Grok and returns a dict with the 6 required keys.
    Raises ValueError if the API fails or returns invalid JSON, so main.py
    can turn that into a proper HTTP error instead of crashing.
    """
    try:
        response = client.chat.completions.create(
            model=GROK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": complaint_text},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        raw_content = response.choices[0].message.content
        result = json.loads(raw_content)

        required_keys = {
            "category", "priority", "location",
            "duration", "problem_summary", "recommended_action",
        }
        if not required_keys.issubset(result.keys()):
            raise ValueError(f"AI response missing required keys. Got: {result.keys()}")

        return result

    except json.JSONDecodeError as e:
        raise ValueError(f"AI did not return valid JSON: {e}")
    except Exception as e:
        raise ValueError(f"AI request failed: {e}")