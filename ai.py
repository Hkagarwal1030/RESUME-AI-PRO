import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key from .env file
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key exists
if not api_key:
    raise RuntimeError(
        "Missing OpenAI API key. Add OPENAI_API_KEY in your .env file."
    )

# Create OpenAI client
client = OpenAI(api_key=api_key)


def analyze_resume(resume_text, user_goal):
    """
    Analyze resume based on user's target role
    """

    prompt = f"""
You are a senior Software Engineer and hiring manager.

Evaluate the resume based on the user's goal.

User Goal: {user_goal}

STRICT RULES:
- Extract only relevant skills for this goal
- Remove irrelevant tools
- Identify missing skills
- Generate roadmap only for missing skills
- Create interview questions based on missing + existing skills

Return ONLY valid JSON in this exact format:

{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": []
}}

Resume:
{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
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

        return json.loads(json_data)

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