from flask import Flask, render_template, jsonify, Response, send_from_directory
import os
import json
import time
from datetime import datetime

app = Flask(__name__)

AUDIO_DIR = "audio"
STT_DIR = "stt"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/get-initial-data")
def get_initial_data():
    date = datetime.now().strftime("%Y-%m-%d")
    stt_file = os.path.join(STT_DIR, f"{date}.json")

    if os.path.exists(stt_file):
        with open(stt_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    return jsonify(data)

@app.route("/stream")
def stream():
    def event_stream():
        last_timestamp = None
        while True:
            date = datetime.now().strftime("%Y-%m-%d")
            stt_file = os.path.join(STT_DIR, f"{date}.json")

            if os.path.exists(stt_file):
                with open(stt_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if data and (last_timestamp is None or data[-1]["timestamp"] != last_timestamp):
                    last_timestamp = data[-1]["timestamp"]
                    yield f"data: {json.dumps(data[-1])}\n\n"

            time.sleep(1)

    return Response(event_stream(), content_type='text/event-stream')

@app.route("/audio/<path:filename>")
def serve_audio(filename):
    folder, file = os.path.split(filename)
    return send_from_directory(os.path.join(AUDIO_DIR, folder), file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
