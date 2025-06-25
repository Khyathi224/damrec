from flask import Flask, request, jsonify, send_from_directory
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploaded_images'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route("/report", methods=["POST"])
def report_issue():
    image = request.files.get('image')
    department = request.form.get('department')
    description = request.form.get('description')
    location = request.form.get('location')

    if not image or not department or not location:
        return jsonify({"error": "Missing fields"}), 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (department, description, location, image_path) VALUES (?, ?, ?, ?)",
                   (department, description, location, image_path))
    conn.commit()
    conn.close()

    return jsonify({"message": "Report submitted successfully"}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return jsonify({"message": "Backend running successfully"})

# Run locally
if __name__ == "__main__":
    app.run(debug=True)
