## 📘 PocketDoc AI — On-Device Document Summarizer & Q&A Assistant

**PocketDoc AI** is a lightweight Python app that reads your documents, summarizes them, and intelligently answers your questions — all locally, directly on your mobile device (via **Pydroid3**).

It works in real time when the program is running and shuts down automatically after exit — no internet, no server, and no external API required.

---

### ⚙️ How It Works

1. **Run the Python script** in Pydroid3.
2. **App starts on a local address** (e.g., `http://127.0.0.1:5000` or `localhost:8501`).
3. **Upload a document (PDF/DOCX)** or paste text.
4. **Get summary instantly.**
5. **Ask any question** — the app answers intelligently from within your document.

---

### 🧠 Features

* 🧾 Reads PDFs and Word documents
* 🧠 Generates concise summaries
* 💬 Answers questions contextually
* 💡 Runs completely offline
* ⚡ Works directly on Android (via Pydroid3)

---

### 🪶 Requirements

Create a file named **`requirements.txt`** in your project folder and paste this inside:

transformers==4.46.0
torch==2.4.1
PyMuPDF==1.24.9
python-docx==1.1.2
docx2txt==0.8
nltk==3.9.1
tqdm==4.66.5
```

---

### ▶️ Installation (on Pydroid3)

1. Open **Pydroid3 Terminal**.
2. Navigate to your project folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run your main file:

   ```bash
   python pocketdoc_ai.py
   ```
5. Wait for a local address to appear (example: `http://127.0.0.1:5000`) and open it in your mobile browser.


### 💡 Example Usage Code

```python
from transformers import pipeline

# Summarizer
summarizer = pipeline("summarization")

# Q&A Model
qa_model = pipeline("question-answering")

# Example usage
text = open("document.txt", "r").read()
summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
print("Summary:", summary[0]['summary_text'])

question = "What is the main topic?"
answer = qa_model(question=question, context=text)
print("Answer:", answer['answer'])



### 👨‍💻 Author

**Abuzar Zafar Dharamkhail**
🇵🇰 Gilgit-Baltistan, Pakistan
🎯 Aspiring AI Researcher | Future MBZUAI Scholar
💡 Focused on creating AI tools that save people’s time and simplify information access.

---

### 🌍 Vision

PocketDoc AI shows how **lightweight, mobile-friendly AI** can make document understanding accessible anywhere — even without high-end hardware or constant internet.

> “True intelligence is in understanding — not in complexity.”


 
