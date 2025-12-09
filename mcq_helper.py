import time
import requests
import clipboard
from plyer import notification

API_URL = "http://127.0.0.1:8000/mcq"  # Backend FastAPI endpoint
last_text = ""

def send_to_api(question):
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
