from flask import Flask, render_template, url_for, request, jsonify
import os
import json

app = Flask(__name__)

@app.route("/")
def index():
    font_images_dir = "static/font_images"
    font_images = [url_for('static', filename=f'font_images/{f}') for f in os.listdir(font_images_dir) if f.endswith(".png")]
    font_images = font_images[:300]  # Limit to the first 300 images

    # Load saved labels
    if os.path.exists("labels.json") and os.path.getsize("labels.json") > 0:
        with open("labels.json", "r") as f:
            saved_labels = json.load(f)
    else:
        saved_labels = []

    return render_template('index.html', font_images=font_images, saved_labels=saved_labels)

@app.route("/save_labels", methods=["POST"])
def save_labels():
    labels = request.json
    with open("labels.json", "w") as f:
        json.dump(labels, f)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)