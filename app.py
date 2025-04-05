from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드 및 API 키 설정
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/correct', methods=['POST'])
def correct_sentence():
    user_input = request.json.get("sentence")

    if not user_input:
        return jsonify({"error": "No sentence provided"}), 400

    prompt = f"""
    Please correct the following English sentence, make it more natural, and explain the grammar mistakes:
    "{user_input}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-4"
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        return jsonify({"result": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

