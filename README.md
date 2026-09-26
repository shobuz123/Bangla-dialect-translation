# Bidirectional Bangla Dialect Translation System

A machine translation system that translates between **Standard Bangla** and four regional dialects — **Sylheti, Chittagonian, Mymensingh, and Noakhali** — using fine-tuned seq2seq transformer models, a retrieval-augmented correction layer, and a full-stack web application.

> Developed as a CSE445 (Machine Learning) capstone project at **North South University**, later extended into a research paper submitted to **ICCIT 2026** (29th IEEE Bangladesh Section Conference, Cox's Bazar).

---

## ✨ Overview

Standard Bangla NLP tools perform poorly on regional dialects due to lexical, phonetic, and grammatical divergence. This project benchmarks five transformer-based seq2seq models on a parallel corpus of dialect–standard sentence pairs, adds a semantic retrieval correction layer to reduce mistranslations, and wraps everything in an interactive web app.

**Key components:**
- 🔤 Five fine-tuned translation models (bidirectional)
- 🔍 RAG-based correction layer using sentence embeddings
- 🌐 Flask web application with voice input/output
- 🤖 MCP server integration for use as a Claude Desktop tool

---

## 📊 Model Performance

| Model       | BLEU  | chrF  |
|-------------|:-----:|:-----:|
| NLLB-200    | 91.46 | 95.42 |
| mBART-50    | 76.03 | 84.59 |
| BanglaT5    | 51.78 | 68.22 |
| IndicBART   | 13.92 | 34.58 |
| mT5-base    |  6.29 | 16.59 |

*Corpus: ~3,933 parallel sentence pairs across Standard Bangla and four dialects.*

---

## 🧠 Models Used

- [NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)
- [mBART-large-50](https://huggingface.co/facebook/mbart-large-50)
- [BanglaT5](https://huggingface.co/csebuetnlp/banglat5)
- [IndicBART](https://huggingface.co/ai4bharat/IndicBART)
- [mT5-base](https://huggingface.co/google/mt5-base)

> 🔗 **Fine-tuned model weights:** hosted separately on Hugging Face Hub (not in this repo due to GitHub file size limits).
> Links: *coming soon*

---

## 🏗️ Project Structure

```
dialect_project/
├── app.py                     # Flask web application entry point
├── translator.py              # Core translation logic
├── models_db.py                # Database models
├── mcp_server.py               # MCP server for Claude Desktop integration
├── shobuz_3models/             # BanglaT5, mT5-base, mBART-50 (configs + results)
├── mate_2models (1)/           # NLLB-200, IndicBART (configs + results)
├── templates/                  # Flask HTML templates
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── translate.html
│   └── base.html
├── static/
│   └── style.css
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/shobuz123/Bangla-dialect-translation.git
cd Bangla-dialect-translation
pip install -r requirements.txt
```

### Run the web app

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

### Run the MCP server (Claude Desktop integration)

```bash
pip install "mcp<2"
python mcp_server.py
```

---

## 💻 Web App Features

- 🔐 User login & registration
- 📜 Translation history dashboard
- 🎙️ Voice input/output via Web Speech API
- 🌗 Glassmorphism dark-gradient UI
- 💾 SQLite-backed persistence

---

## 👤 Author

**Mahedi Hasan Shobuz**

*Supervised by Mr. Intisar Tahmid Naheen, Senior Lecturer, North South University.*

---

## 📄 Publication

This work was submitted to **ICCIT 2026** (29th IEEE Bangladesh Section Conference), Track 1: AI/ML/Algorithms/Data Science.

---

## 📌 Roadmap

- [ ] Publish fine-tuned weights to Hugging Face Hub
- [ ] arXiv preprint
- [ ] Extended journal version
- [ ] Submission to BLP Workshop (ACL Bangla Language Processing)

---

## 📜 License

This project is for academic and research purposes.
