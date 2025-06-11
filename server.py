from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyCPxYEmoEf0CNHWXO8yIKKATzgoYEpby-E"  # Replace with your API key

def get_gemini_answer(question_with_options):
    prompt = f"""{question_with_options}

    Select the correct answer from the options above. Only respond with the option letter or exact answer text."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "Could not extract answer from Gemini API response."

@app.route('/question', methods=['POST'])
def question():
    data = request.json
    question_text = data.get("question", "")
    print("Received question:", question_text)
    answer = get_gemini_answer(question_text)
    print("Answer:", answer)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=5000)