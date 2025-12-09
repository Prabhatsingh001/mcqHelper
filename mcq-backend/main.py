from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"   # remove "models/" prefix here

app = FastAPI()

class MCQRequest(BaseModel):
    question: str

def build_prompt(question: str):
    return f"""
Solve this MCQ.

Return ONLY the correct option letter (A, B, C, or D).
No explanation.

Question:
{question}
"""

@app.post("/mcq")
def solve_mcq(req: MCQRequest):
    prompt = build_prompt(req.question)

    # ✔ correct endpoint
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 5
        }
    }

    response = requests.post(url, json=payload)

    # ✔ Print raw text for debugging if needed
    print("RAW RESPONSE TEXT:", response.text)

    # ✔ Prevent crash if no JSON
    if not response.text:
        return {"answer": "Error: Empty response from Gemini"}

    data = response.json()

    print("FULL JSON:", data)

    try:
        answer = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return {"answer": f"Error parsing response: {e}"}

    return {"answer": answer.replace("Answer:", "").strip()}
