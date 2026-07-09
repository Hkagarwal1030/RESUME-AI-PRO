import os
import json
import ast
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key from .env file
api_key = os.getenv("OPENROUTER_API_KEY")


# Check if API key exists
if not api_key:
    raise RuntimeError(
        "Missing OpenRouter API key. Add OPENROUTER_API_KEY in your .env file."
    )

# Create OpenAI client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

def analyze_resume(resume_text, user_goal):
    """
    Analyze resume based on user's target role
    """

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
        response = client.chat.completions.create(
            model = "openai/gpt-oss-20b:free",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict hiring manager."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

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
            "error": "Invalid JSON response from AI"
        }

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }
    
    print(api_key)