from flask import Flask, jsonify, request, redirect
from app.utils import generate_id, is_url_valid
from app.models import save_url, increment_click_count, get_stats
from app.store import url_db

app = Flask(__name__)
BASE_URL = "http://127.0.0.1:5000/"


@app.route("/")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })


@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url or not is_url_valid(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Generate unique short ID
    short_id = generate_id()
    while short_id in url_db:
        short_id = generate_id()

    save_url(short_id, original_url)

    return jsonify({
        "short_url": BASE_URL + short_id,
        "short_id": short_id,
        "long_url": original_url
    }), 201


@app.route("/<short_id>")
def redirect_to_url(short_id):
    if short_id not in url_db:
        return jsonify({"error": "URL not found"}), 404

    increment_click_count(short_id)
    return redirect(url_db[short_id]["long_url"])


@app.route("/api/stats/<short_id>")
def url_stats(short_id):
    try:
        stats = get_stats(short_id)
        return jsonify(stats)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
