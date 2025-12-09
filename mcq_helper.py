"""MCQ Helper - Clipboard-based MCQ Question Solver.

This module monitors the system clipboard for multiple choice questions and
automatically sends them to the backend API for solving. It displays answers
as desktop notifications.

Attributes:
    API_URL (str): The URL of the backend FastAPI endpoint for MCQ solving.
    last_text (str): Stores the last clipboard content to detect changes.
"""
import time
import requests
import clipboard
from plyer import notification

API_URL = "http://127.0.0.1:8000/mcq"  # Backend FastAPI endpoint
last_text = ""


def send_to_api(question):
    """Send MCQ question to the backend API for solving.

    Sends a POST request to the FastAPI backend with the MCQ question
    and returns the answer received from the API.

    Args:
        question (str): The MCQ question text to be solved.

    Returns:
        str: The answer from the backend (typically a single letter A, B, C, or D),
             or an error message if the request fails.

    Example:
        >>> answer = send_to_api("What is 2+2? A)3 B)4 C)5 D)6")
        >>> print(answer)
        'B'
    """
    try:
        resp = requests.post(API_URL, json={"question": question})
        
        if resp.status_code != 200:
            return f"Backend error: {resp.status_code}"
        
        data = resp.json()
        answer = data.get("answer", "").strip()
        
        return answer if answer else "No answer returned"

    except Exception as e:
        return f"Error contacting backend: {e}"

print("MCQ Helper running... Highlight text & press CTRL+C to get answers instantly.")

while True:
    try:
        text = clipboard.paste().strip()
        if text != last_text and len(text) > 5:
            last_text = text

            print("\nDetected MCQ:")
            print(text)
            print("Requesting answer...")

            answer = send_to_api(text)

            print("Answer:", answer)

            notification.notify(
                title="",
                message=answer,
                timeout=5
            ) # type: ignore

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
