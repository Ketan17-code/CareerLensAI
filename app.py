from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from analyzer import analyze_resume
from pathlib import Path

app = Flask(__name__)
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED = {"pdf", "docx", "txt"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "Please upload a resume."}), 400
    file = request.files["resume"]
    role = request.form.get("role", "AI/ML Engineer")
    if not file.filename:
        return jsonify({"error": "No file selected."}), 400
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED:
        return jsonify({"error": "Only PDF, DOCX and TXT files are supported."}), 400

    safe_name = secure_filename(file.filename)
    path = UPLOAD_FOLDER / safe_name
    file.save(path)
    try:
        result = analyze_resume(path, role)
        result["filename"] = safe_name
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
