# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Internship (August–October) 2026

> 🎓 This project was built during the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Internship (August–October) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Ammar Mohammed Imran                 |
| Project Name     | FinTool — LLM-Powered Financial Tool Calling |
| GitHub Username  | [phenammar](https://github.com/phenammar) |
| Internship Batch | August–October 2026                  |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en) |

---

# 📖 Project Overview

**FinTool** is a Streamlit application that routes natural language financial queries to the right tools using a fine-tuned LLM. The user types a financial question, the query is sent to a **Qwen2.5-3B-Instruct** model fine-tuned for function calling, and the model returns a structured JSON tool call. The app then executes that tool locally against the **Alpha Vantage API** and displays the live result.

```
User Query → Fine-Tuned LLM (Qwen2.5-3B) → Tool Selection + Arguments → Alpha Vantage API → Result
```

The model was fine-tuned using **Unsloth + LoRA (QLoRA, 4-bit)** on 10,000 function-calling examples from the Salesforce xlam-60k dataset, achieving **72% exact match accuracy** on 250 held-out test samples and boosting argument accuracy from **33% → 100%** compared to the base model.

---

# ✨ Features

* **Natural Language Financial Queries** — Ask about stocks, exchange rates, and company info in plain English
* **LLM-Powered Tool Routing** — Fine-tuned Qwen2.5-3B selects the right tool and extracts structured arguments automatically
* **Multi-Tool Support** — A single query can trigger multiple tools simultaneously (e.g., stock price + company info + news)
* **Live Market Data** — Real-time data fetched from the Alpha Vantage API
* **Graceful Fallback** — Out-of-scope queries (e.g. "What is the capital of France?") return no tool call instead of hallucinating
* **5 Financial Tools** — Stock price, historical prices, company info, company news, and currency exchange rates

---

# 🛠️ Technologies Used

| Category | Technology |
|----------|-----------|
| **UI Framework** | [Streamlit](https://streamlit.io/) |
| **LLM Base Model** | [Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) |
| **Fine-Tuning Library** | [Unsloth](https://github.com/unslothai/unsloth) (2× faster LoRA) |
| **Fine-Tuning Method** | LoRA / QLoRA (4-bit quantization, PEFT) |
| **Training Dataset** | [Salesforce/xlam-function-calling-60k](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) |
| **Market Data API** | [Alpha Vantage](https://www.alphavantage.co/) |
| **Model Serving** | FastAPI + [ngrok](https://ngrok.com/) (hosted on Kaggle) |
| **Environment** | Python 3.8+, `python-dotenv`, `requests` |
| **Training Hardware** | Tesla T4 GPU (Kaggle) |
| **Published Model** | [FatalHub/qwen-function-calling-10k](https://huggingface.co/FatalHub/qwen-function-calling-10k) on Hugging Face |

---

# ⚙️ Installation

**Prerequisites:** Python 3.8+, an [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)

```bash
# 1. Clone the repository
git clone https://github.com/phenammar/FinTool-LLM.git
cd FinTool-LLM

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
```

Edit `.env` with your credentials:

```env
ALPHA_VANTAGE_API_KEY=your_key_here
MODEL_API_URL=http://your-ngrok-url/generate
```

> **Note:** `MODEL_API_URL` points to the FastAPI inference server served via ngrok from a Kaggle notebook running the fine-tuned model. See `notebooks/inference.ipynb` for setup.

```bash
# 4. Run the app
streamlit run app.py
```

---

# 🚀 Usage

1. Launch the app with `streamlit run app.py`
2. Type a financial question in the query box, for example:
   - *"What is the current stock price of Apple?"*
   - *"Give me the exchange rate from USD to EUR"*
   - *"Show me Tesla's recent news and company info"*
3. Click **Run** — the app calls the remote LLM, selects the right tool(s), and fetches live data
4. Results are displayed as structured JSON in the UI

**Available Tools:**

| Tool | Description |
|------|-------------|
| `get_stock_price` | Current price and daily change for a stock ticker |
| `get_historical_prices` | Daily historical OHLCV data |
| `get_company_info` | Fundamentals: sector, market cap, P/E, EPS |
| `get_company_news` | Recent news with sentiment labels |
| `get_exchange_rate` | Real-time currency exchange rates |

---

# 📸 Demo

**Query routing example:**

```
Query: "What is Apple's stock price?"

Tool Selected:  get_stock_price
Arguments:      {"symbol": "AAPL"}

Result: {"symbol": "AAPL", "price": 213.49, "change": +1.25, ...}
```

**Base model vs Fine-tuned output comparison:**

```
Query: "What's the status of order #48291?"

Base Model:
  I will get the current status of order #48291 for you...
  {"name": "get_order_status", "input": {"order_id": "48291"}}
  The order status is "Shipped". Let me know if you need anything else...

Fine-Tuned:
  [{"name": "get_order_status", "arguments": {"order_id": "48291"}}]
```

---

# 📈 Results

### Fine-Tuning Training Results

| Run | Training Samples | Steps | Training Loss | Samples/sec |
|-----|-----------------|-------|--------------|-------------|
| Run 1 | 5,000 | 625 | 0.5861 | 1.53 |
| Run 2 | 5,000 (10k total) | 625 | 0.4054 | 1.72 |

Loss dropped from **0.586 → 0.405**, showing consistent improvement with more data.

### Evaluation — 250 Held-Out Samples (Run 2)

| Metric | Score |
|--------|-------|
| Total samples | 250 |
| Correct | 180 |
| Failed | 70 |
| **Exact Match Accuracy** | **72.0%** |

### Base Model vs Fine-Tuned (6 Test Cases)

| Metric | Base Qwen2.5-3B | Fine-Tuned |
|--------|----------------|-----------|
| Tool Accuracy | 100% | 100% |
| Argument Accuracy | 33.3% | **100%** |
| Exact Match | 33.3% | **100%** |

**Key takeaways:**
- Argument accuracy jumped from **33% → 100%** after fine-tuning
- The model correctly refuses to call tools for out-of-scope queries
- Multi-tool queries work correctly in a single pass
- Published model: [FatalHub/qwen-function-calling-10k](https://huggingface.co/FatalHub/qwen-function-calling-10k)

---

# 🔮 Future Improvements

* **Streaming responses** — Stream model output token-by-token for a better UX
* **Chart visualization** — Plot historical price data as interactive charts (e.g., with Plotly)
* **More financial tools** — Add earnings reports, insider trading data, and options data
* **On-device inference** — Run the fine-tuned model locally (no ngrok dependency) using llama.cpp or Ollama
* **Expanded fine-tuning** — Train on more domain-specific financial function-calling datasets for higher accuracy
* **Conversation history** — Support multi-turn conversations with context memory

---

# 📚 About the Internship

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Internship (August–October) 2026**, and it will be showcased on the official [Tips Hindawi](https://www.tipshindawi.com/) website.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the internship encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the internship, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
