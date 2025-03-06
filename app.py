from flask import Flask, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use Render's PostgreSQL database URL from environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "not_set")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define the database model
class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    font_images_dir = "static/font_images"
    font_images = [url_for('static', filename=f'font_images/{f}') for f in os.listdir(font_images_dir) if f.endswith(".png")]
    font_images = font_images[:300]  # Limit to the first 300 images

    # Load saved labels from PostgreSQL
    saved_labels_query = Label.query.all()
    saved_labels = [{"image_url": label.image_url, "label": label.label} for label in saved_labels_query] if saved_labels_query else []

    return render_template('index.html', font_images=font_images, saved_labels=saved_labels)

@app.route("/save_labels", methods=["POST"])
def save_labels():
    try:
        data = request.json  # Expecting a list of dictionaries
        print('Received labels to save:', data)  # Debugging log

        # Clear old labels
        Label.query.delete()
        db.session.commit()

        # Save new labels
        for item in data:
            if isinstance(item, dict) and "image_url" in item and "label" in item:
                new_label = Label(image_url=item["image_url"], label=item["label"])
                db.session.add(new_label)
            else:
                raise ValueError("Invalid data format")

        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        print('Error saving labels:', e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)