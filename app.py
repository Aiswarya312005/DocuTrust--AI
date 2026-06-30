from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from pypdf import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Replace with your Gemini API key
genai.configure(api_key="Your_API_Key")

model = genai.GenerativeModel("gemini-2.5-flash")

document_text = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    global document_text

    if "pdf" not in request.files:
        return jsonify({"message": "No file selected"}), 400

    file = request.files["pdf"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    document_text = text

    print("PDF Uploaded")
    print("Text Length:", len(document_text))

    return jsonify({
        "message": "PDF Uploaded Successfully"
    })

@app.route("/ask", methods=["POST"])
def ask():

    global document_text

    if not document_text:
        return jsonify({
            "answer": "Please upload a PDF first."
        })

    print("Question received")

    question = request.json["question"]

    print("Question:", question)
    print("Document Length:", len(document_text))

    prompt = f"""
Answer only using the document below.

Document:
{document_text}

Question:
{question}
"""

    try:
        response = model.generate_content(prompt)

        print("Response Generated")

        return jsonify({
            "answer": response.text
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "answer": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)