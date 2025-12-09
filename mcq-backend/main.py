"""MCQ Solver Backend API using Google Gemini.

This module provides a FastAPI server that solves multiple choice questions
using Google's Gemini AI model. It receives MCQ questions via HTTP POST requests
and returns the correct answer option.

Attributes:
    GEMINI_API_KEY (str): API key for Google Gemini authentication.
    MODEL (str): The Gemini model version to use for solving MCQs.
    app (FastAPI): FastAPI application instance.
"""
from fastapi import FastAPI
from dotenv import load_dotenv
from schemas import MCQRequest
import os
import requests
from utils import build_prompt

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

app = FastAPI()


@app.post("/mcq")
def solve_mcq(req: MCQRequest):
    """Solve a multiple choice question using Google Gemini API.

    Sends the MCQ question to the Gemini API with a prompt instructing it to
    return only the correct answer option (A, B, C, or D).

    Args:
        req (MCQRequest): Request object containing the MCQ question.

    Returns:
        dict: A dictionary with the 'answer' key containing the correct option
              letter, or an error message if processing fails.

    Example:
        >>> response = solve_mcq(MCQRequest(question="What is 2+2? A)3 B)4 C)5 D)6"))
        >>> print(response["answer"])
        'B'
    """
    prompt = build_prompt(req.question)
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
    if not response.text:
        return {"answer": "Error: Empty response from Gemini"}
    data = response.json()
    try:
        answer = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return {"answer": f"Error parsing response: {e}"}

    return {"answer": answer.replace("Answer:", "").strip()}
