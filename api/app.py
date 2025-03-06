from flask import Flask, request, render_template, send_from_directory, jsonify
import os
import cv2
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None, "Error: Could not read the image."

    # Dummy bounding box (change this with your actual model output)
    height, width, _ = image.shape
    start_point = (width // 4, height // 4)
    end_point = (width * 3 // 4, height * 3 // 4)
    color = (0, 255, 0)  # Green color
    thickness = 2

    cv2.rectangle(image, start_point, end_point, color, thickness)

    processed_filename = "processed_" + os.path.basename(image_path)
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    cv2.imwrite(processed_path, image)

    return processed_filename, None

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    processed_filename, error = process_image(file_path)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"processed_image": f"/static/processed/{processed_filename}"})

if __name__ == "__main__":
    app.run(debug=True)
