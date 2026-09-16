from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get('symbol', '')
    price = data.get('price', '')
    message = data.get('message', '')
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1024,
            "messages": [{
                "role": "user",
                "content": f"تحلیل کن: {symbol} در قیمت {price}. سیگنال: {message}"
            }]
        }
    )
    result = response.json()
    analysis = result['content'][0]['text']
    return jsonify({"status": "ok", "analysis": analysis})

@app.route('/', methods=['GET'])
def home():
    return "سرور فعاله! ✅"

if __name__ == '__main__':
    app.run(port=5000)
