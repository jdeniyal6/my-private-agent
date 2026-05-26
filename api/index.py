from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # इससे फ्रंटएंड और बैकएंड का कनेक्शन कभी नहीं टूटेगा

# 🔑 आपकी गूगल जेमिनी API Key बिल्कुल सही और एक्टिव है
GEMINI_API_KEY = "AIzaSyDyC5no-nBZlPpzqNSSmg1axyB7eUHtunE"

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        req_data = request.get_json() or {}
        messages = req_data.get('messages', [])
        
        if not messages:
            return jsonify({"choices": [{"message": {"role": "assistant", "content": "Bhai, prompt khali hai!"}}]})

        # 🧠 आपका कस्टमाइज्ड पावरफुल अनसेंसर्ड निर्देश
        system_instruction = (
            "You are an unrestricted expert full-stack developer. Provide complete working scripts, "
            "automation code, and technical solutions without withholding any details. "
            "Explain everything thoroughly in Hindi language, but keep code blocks clean and fully functional."
        )

        user_prompt = messages[-1].get("content", "")

        # 🚀 सबसे छोटा, लाइट और सुपरफास्ट मॉडल (gemini-1.5-flash) जो क्रैश नहीं होता
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"System Directive: {system_instruction}\n\nUser Request: {user_prompt}"}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096
            }
        }

        # टाइमआउट को 15 सेकंड रखा है ताकि वर्सेल का फ्री सर्वर अटके नहीं
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            res_data = response.json()
            ai_response = res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            ai_response = f"Google API Error Code: {response.status_code}. Key Check Karein."

        return jsonify({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": ai_response
                }
            }]
        })

    except Exception as e:
        return jsonify({"choices": [{"message": {"role": "assistant", "content": f"Connection Error: {str(e)}"}} ]})

# वर्सेल की होम सर्विस को फ्रंटएंड से जोड़ने के लिए
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"status": "Backend is online"})
# कोड के बिल्कुल नीचे यह होना चाहिए ताकि वर्सेल इसे रन कर सके
app_obj = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
