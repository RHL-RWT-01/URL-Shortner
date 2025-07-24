from flask import Flask, jsonify
import re
app = Flask(__name__)

url_db = {}
click_count = {}

BASE_URL = "https://short.ly/"
URL_REGEX = re.compile(
    r'^(https?://)?'        
    r'([\da-z.-]+)\.([a-z.]{2,6})'
    r'([/\w .-]*)*/?$' 
)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)