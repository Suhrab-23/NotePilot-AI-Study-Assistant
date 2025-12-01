# 📚 NotePilot - AI Study Assistant

Suhrab Roeen 100811513

NotePilot is an AI-powered study companion that helps students understand their course materials through intelligent summarization, interactive Q&A, and practice quizzes. Built with Flask, RAG (Retrieval-Augmented Generation), and local Ollama models for privacy and cost-free operation.

## 🎯 Features

### Core Functionality
- **📄 Smart PDF Summarization**: Upload lecture notes and get AI-generated summaries with formatted markdown display
- **💬 RAG-Powered Q&A**: Ask questions with context-aware answers using sentence-transformers + FAISS vector search
- **🎯 Practice Quiz Generation**: Auto-generate 3 multiple-choice questions with explanations and instant feedback
- **📚 Sample Data**: One-click loading of sample ML notes for instant demo

### Technical Implementation
- **Safety & Robustness**: Input validation (2000 char limit), prompt injection detection (9 patterns), system prompt enforcement
- **Telemetry Logging**: JSON logs with timestamp, pathway, and latency for all requests
- **Offline Evaluation**: 17 test cases across 5 categories with automated pass/fail reporting (100% pass rate achieved)
- **Clean Architecture**: Server-side session storage, automatic file cleanup, graceful error handling

## 📋 Prerequisites

1. **Python 3.8+** (tested with Python 3.11)
2. **Ollama** installed and running locally
   - Download from: https://ollama.ai/
   - Pull a model: `ollama pull llama3.2:latest` (or llama3.2:1b for faster responses)

## 🚀 Quick Start

### Option 1: One-Command Run (Recommended)

```powershell
python run.py
```

This script will:
- ✅ Check if Ollama is running
- ✅ Offer to install dependencies if needed
- ✅ Start the Flask server on http://localhost:5000

### Option 2: Manual Setup

1. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Start Ollama** (separate terminal)
   ```powershell
   ollama serve
   ```

3. **Run the app**
   ```powershell
   python app.py
   ```

4. **Open browser**: http://localhost:5000

## 📝 Usage

### Quick Demo (No PDF Required)
1. Navigate to http://localhost:5000
2. Click **"📚 Use Sample ML Notes PDF"** button
3. Wait ~10 seconds for processing
4. Explore the summary, ask questions, generate a quiz!

### Upload Your Own PDF
1. Click the upload area or drag-and-drop a PDF
2. Wait for AI to process and summarize your notes
3. Use the three-panel interface:
   - **Left**: Generate quizzes, upload new documents
   - **Center**: Read formatted AI summary with markdown
   - **Right**: Ask questions about your notes

### Interactive Features
- **Chat**: Type questions like "What are the main topics?" or "Explain concept X"
- **Quiz**: Generate 3 multiple-choice questions with randomized correct answers
- **Single-Question Flow**: Submit answers, see explanations, track your score

**Note**: PDFs must contain selectable text. Image-only or handwritten PDFs are not supported.

## 🧪 Testing & Evaluation

### Run Offline Tests

```powershell
python eval_tests.py
```

**Test Coverage** (17 test cases):
- ✅ Input validation: empty inputs, single chars, whitespace-only
- ✅ Prompt injection: 6 different attack patterns ("ignore previous", "you are now", etc.)
- ✅ Input length: at limit (2000 chars), exceeding limit (2001 chars)
- ✅ Normal questions: 5 valid educational queries
- ✅ Edge cases: additional boundary conditions

**Results**: 100% pass rate (17/17 tests passing)

Expected output:
```
======================================================================
NotePilot - Offline Evaluation Suite
======================================================================
Total Tests:  17
Passed:       17 (100.0%)
Failed:       0
✓ All tests PASSED (100% pass rate)
```

## 📊 Telemetry

All requests are logged to `logs/telemetry.json` with:
- `timestamp`: ISO 8601 format (e.g., "2025-11-30T14:32:15.123456")
- `pathway`: Request type (`upload_summarize`, `upload_sample`, `chat_rag`, `quiz_generation_rag`, error pathways)
- `latency_seconds`: Processing time (float)

Example log entry:
```json
{
  "timestamp": "2025-11-30T17:25:51.666889",
  "pathway": "quiz_generation_rag",
  "latency_seconds": 11.982
}
```

**Typical Latencies**:
- PDF upload + summary: 8-12 seconds
- Chat query (RAG): 2-4 seconds
- Quiz generation: 3-7 seconds

## 🛡️ Safety & Guardrails

1. **System Prompt**: Explicit rules for educational assistance only
2. **Input Validation**:
   - Max 2000 characters per query
   - Rejects empty/whitespace-only inputs
3. **Prompt Injection Detection**: Blocks attempts to:
   - "ignore previous instructions"
   - "you are now..."
   - "disregard previous"
   - And 6+ other patterns
4. **Error Handling**: Graceful fallback messages for API failures

## 📁 Project Structure

```
notepilot/
├── app.py                      # Main Flask application with RAG pipeline
├── run.py                      # One-command startup script
├── requirements.txt            # Python dependencies (Flask, sentence-transformers, FAISS, etc.)
├── .env.example               # Environment configuration (included for easy setup)
├── README.md
├── TECH_NOTE.md               # Technical documentation with architecture diagram
├── templates/
│   ├── index.html            # Landing page with upload + sample PDF button
│   └── main.html             # Three-panel interface (sidebar, summary, chat)
├── tests/
│   └── tests.json            # 17 test cases for offline evaluation
├── eval_tests.py             # Automated test runner with pass rate reporting
├── data/
│   └── sample_ml_notes.pdf   # Seed data for demo (machine learning notes)
├── uploads/                  # Temporary storage for uploaded PDFs (auto-deleted after processing)
└── logs/
    └── telemetry.json        # JSON logs (timestamp, pathway, latency)
```

## 🔧 Configuration

### Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `my-secret-key` | Flask session encryption key |
| `OLLAMA_API_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.2:latest` | Ollama model name |

**Note**: `.env.example` is included in the repo with working defaults. No configuration changes needed for basic usage!

## 🔍 Troubleshooting

### Ollama not running
```powershell
# Start Ollama in a new terminal
ollama serve
```

### Model not found
```powershell
# Pull the model
ollama pull llama3.2:1b
```

### Port already in use
Edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 → 5001
```

### Dependency installation fails
```powershell
# Upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### PDF upload fails
- Check file size (max 16MB)
- Ensure PDF is not password-protected
- Try a different PDF with simpler formatting
