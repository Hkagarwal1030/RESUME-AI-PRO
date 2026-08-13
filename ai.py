import os
import json
import ast
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b:free")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

def analyze_resume(resume_text, user_goal):
    """Analyze resume based on user's target role.

    Uses a direct HTTP call to OpenRouter's Chat Completions API to avoid
    runtime dependency incompatibilities with the OpenAI client library.
    """

    if not api_key:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_prep": [],
            "error": "OPENROUTER_API_KEY is missing. Add it to your environment before deploying or testing the app."
        }

    prompt = f"""
You are an experienced hiring manager and career coach for data and analytics professionals.

Evaluate the resume against the user's target role.

User Goal: {user_goal}

STRICT RULES:
- Extract only the most relevant existing skills for this goal.
- Identify the missing skills that will make the candidate competitive.
- Build a clear, attractive learning roadmap using prioritized steps.
- Provide interview prep as question-and-answer pairs.

Return ONLY valid JSON in this exact format:

{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_prep": []
}}

Where "interview_prep" is a list of objects with:
{{"question": "...", "answer": "..."}}

Resume:
{resume_text}
"""

    try:
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model_name,
            "temperature": 0.3,
            "messages": [
                {"role": "system", "content": "You are a strict hiring manager."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 1200,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=(10, 120))
        if resp.status_code == 429:
            return {
                "skills": [],
                "missing_skills": [],
                "roadmap": [],
                "interview_prep": [],
                "error": "OpenRouter is rate-limiting requests right now. Please wait a few minutes and try again, or use a different model/key."
            }

        resp.raise_for_status()
        data = resp.json()

        # Safe extraction similar to the OpenAI response shape
        content = ""
        if isinstance(data, dict):
            choices = data.get("choices") or []
            if choices and isinstance(choices, list):
                first = choices[0]
                # Some providers return message under 'message' or 'delta'
                msg = first.get("message") or first.get("delta") or {}
                if isinstance(msg, dict):
                    content = msg.get("content") or ""
                else:
                    content = first.get("text") or ""
        content = content.strip()

        # Extract JSON safely
        start_index = content.find("{")
        end_index = content.rfind("}") + 1

        if start_index == -1 or end_index == 0:
            raise ValueError("No valid JSON found in AI response")

        json_data = content[start_index:end_index]
        parsed = json.loads(json_data)

        if "interview_prep" not in parsed or not isinstance(parsed["interview_prep"], list):
            parsed["interview_prep"] = []

        if "interview_questions" in parsed and not parsed.get("interview_prep"):
            parsed["interview_prep"] = [
                {"question": q, "answer": ""} for q in parsed.get("interview_questions", [])
            ]

        # Normalize roadmap entries into objects with 'title' and 'description'
        roadmap = parsed.get("roadmap", []) or []
        normalized = []
        for item in roadmap:
            title = None
            description = None
            actions = None

            if isinstance(item, dict):
                title = item.get("title") or item.get("name")
                description = item.get("description") or item.get("desc")
                actions = item.get("actions") or item.get("tasks")

            elif isinstance(item, str):
                txt = item.strip()
                # try parse python-style dict using ast.literal_eval
                if txt.startswith("{") and txt.endswith("}"):
                    try:
                        obj = ast.literal_eval(txt)
                        if isinstance(obj, dict):
                            title = obj.get("title") or obj.get("name")
                            description = obj.get("description") or obj.get("desc")
                            actions = obj.get("actions") or obj.get("tasks")
                    except Exception:
                        pass

                if not title:
                    parts = txt.splitlines()
                    if len(parts) >= 2:
                        title = parts[0].strip()
                        description = " ".join([p.strip() for p in parts[1:] if p.strip()])
                    else:
                        title = txt

            normalized.append({
                "title": title if title else "Step",
                "description": description,
                "actions": actions
            })

        parsed["roadmap"] = normalized

        return parsed

    except json.JSONDecodeError:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": "Invalid JSON response from AI. Please try again in a moment."
        }

    except requests.RequestException as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": f"AI provider request failed: {str(e)}"
        }

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }