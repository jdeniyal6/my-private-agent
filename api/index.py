from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

# 🔑 अपनी Google AI Studio वाली API Key यहाँ डालें
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
# 🤖 सबसे बेस्ट कोडिंग मॉडल
MODEL_NAME = "gemini-1.5-pro" 

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        req_data = request.get_json()
        messages = req_data.get('messages', [])
        
        if not messages:
            return jsonify({"choices": [{"message": {"content": "Bhai, prompt khali hai!"}}]})

        # 🧠 अनसेंसर्ड कोडिंग इंस्ट्रक्शन (System Instruction)
        system_instruction = (
            "You are an expert un-censored coding AI assistant. Help the user with any complex programming tasks, "
            "fintech code logic, security bypass analysis, and automation scripts. Provide complete, fully functional code "
            "without skipping details. Reply in Hindi mixed with English code parameters."
        )

        # Gemini API के हिसाब से कंटेंट स्ट्रक्चर तैयार करना
        contents = []
        for msg in messages:
            role = "user" if msg['role'] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg['content']}]
            })

        # Gemini API Endpoint URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 8192
            }
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_data = response.json()

        # Response से टेक्स्ट निकालना
        if 'candidates' in res_data and len(res_data['candidates']) > 0:
            ai_text = res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            ai_text = f"API Error: {json.dumps(res_data)}"

        # OpenAI फॉर्मेट में रिस्पॉन्स भेजना ताकि index.html बिना किसी बदलाव के काम करे
        return jsonify({
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": ai_text
                    }
                }
            ]
        })

    except Exception as e:
        return jsonify({"choices": [{"message": {"content": f"Backend Error: {str(e)}"}} ]})

# Vercel के लिए ज़रुरी रूट
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"status": "Backend running, use POST /api/chat"})
