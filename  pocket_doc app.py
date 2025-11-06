# Simplified PocketDoc for Pydroid 3
# Run: python pocketdoc_app.py
# Open in browser: http://127.0.0.1:5000 or http://0.0.0.0:5000

import io
from flask import Flask, request, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize

# Download punkt tokenizer if not present
try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")

app = Flask(__name__)

# --- Minimal HTML template ---
HTML = """
<!doctype html>
<title>PocketDoc</title>
<h1>PocketDoc Summarizer & Q&A</h1>

<form method="post" enctype="multipart/form-data" action="/upload">
    <label>Upload PDF (optional):</label><br>
    <input type="file" name="file" accept="application/pdf"><br><br>
    <label>Or paste text:</label><br>
    <textarea name="text" rows="10" cols="60" placeholder="Paste document text here..."></textarea><br><br>
    <button type="submit">Process Document</button>
</form>

{% if summary %}
<hr>
<h3>Summary:</h3>
<p>{{ summary }}</p>

<form method="post" action="/ask">
    <input type="hidden" name="doc_text" value="{{ doc_text|e }}">
    <label>Ask a question about the document:</label><br>
    <input type="text" name="question" style="width:60%" placeholder="e.g., What is the main point?"><br><br>
    <button type="submit">Ask</button>
</form>
{% endif %}

{% if answer %}
<hr>
<h3>Answer:</h3>
<p>{{ answer }}</p>
{% endif %}
"""

# --- Utilities ---
def extract_text_from_pdf(file_stream):
    reader = PyPDF2.PdfReader(file_stream)
    text_parts = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except:
            pass
    return "\n".join(text_parts)

def summarize(text, k=3):
    sents = sent_tokenize(text)
    if len(sents) <= k:
        return " ".join(sents)
    vect = TfidfVectorizer(stop_words='english')
    X = vect.fit_transform(sents)
    scores = X.sum(axis=1).A1
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    top_idx.sort()
    return " ".join([sents[i] for i in top_idx])

def answer_question(text, question, top_k=3):
    sents = sent_tokenize(text)
    corpus = sents + [question]
    vect = TfidfVectorizer(stop_words='english')
    X = vect.fit_transform(corpus)
    q_vec = X[-1]
    sent_vecs = X[:-1]
    sims = cosine_similarity(q_vec, sent_vecs).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    answers = [f"[score={sims[i]:.3f}] {sents[i]}" for i in top_idx]
    return "\n".join(answers)

# --- Flask routes ---
@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    text = request.form.get("text", "").strip()
    doc_text = ""
    if uploaded_file and uploaded_file.filename != "":
        doc_text = extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    if not doc_text and text:
        doc_text = text
    if not doc_text:
        return render_template_string(HTML)
    summary_text = summarize(doc_text, k=3)
    return render_template_string(HTML, summary=summary_text, doc_text=doc_text)

@app.route("/ask", methods=["POST"])
def ask():
    doc_text = request.form.get("doc_text", "")
    question = request.form.get("question", "")
    if not doc_text or not question:
        return render_template_string(HTML)
    ans = answer_question(doc_text, question, top_k=3)
    summary_text = summarize(doc_text, k=3)
    return render_template_string(HTML, summary=summary_text, doc_text=doc_text, answer=ans)

if __name__ == "__main__":
    # Use 0.0.0.0 for Pydroid 3 to make sure the browser connects
    app.run(host="0.0.0.0", port=5000)