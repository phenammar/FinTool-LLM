# FinTool — LLM-Powered Financial Tool Calling

A Streamlit application that routes natural language financial queries to the right tools using a fine-tuned LLM. The model reads the query, selects the appropriate tool(s), extracts arguments, and returns live data from the Alpha Vantage API.

---

## How It Works

```
User Query → Fine-Tuned LLM (Qwen2.5-3B) → Tool Selection + Arguments → Alpha Vantage API → Result
```

1. The user types a financial question (e.g. *"What is Apple's stock price?"*)
2. The query is sent to a remote model endpoint (hosted on Kaggle via ngrok)
3. The model returns a structured JSON tool call
4. The app executes the tool locally using the Alpha Vantage API
5. The result is displayed in the UI

---

## Available Tools

| Tool | Description |
|------|-------------|
| `get_stock_price` | Current price and daily change for a stock ticker |
| `get_historical_prices` | Daily historical OHLCV data |
| `get_company_info` | Fundamentals: sector, market cap, P/E, EPS |
| `get_company_news` | Recent news with sentiment labels |
| `get_exchange_rate` | Real-time currency exchange rates |

---

## Project Structure

```
Handler/
├── app.py              # Streamlit UI and main orchestration
├── model_client.py     # HTTP client for the remote LLM API
├── tool_executor.py    # Dispatches tool calls to implementations
├── tool_schemas.py     # JSON schemas for all tools
├── prompt.py           # System prompt construction
├── tools/
│   ├── stock_price.py
│   ├── historical_prices.py
│   ├── company_info.py
│   ├── company_news.py
│   └── exchange_rate.py
├── notebooks/          # Fine-tuning and evaluation experiments
└── requirements.txt
```

---

## Setup

**Prerequisites:** Python 3.8+, an [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
```

Edit `.env`:

```env
ALPHA_VANTAGE_API_KEY=your_key_here
MODEL_API_URL=http://your-ngrok-url/generate
```

```bash
# 3. Run the app
streamlit run app.py
```

---

## Fine-Tuning Report

The LLM powering tool selection is **Qwen2.5-3B-Instruct** fine-tuned for function calling. This section summarizes the training pipeline and results from the notebooks in [`notebooks/`](notebooks/).

### Dataset

- **Source:** [Salesforce/xlam-function-calling-60k](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) — 60,000 function-calling examples
- **Training:** Two sequential runs of 5,000 examples each (10,000 total)
- **Validation / Test:** 250 examples each per run

Training format used:

```
Tools:
[{"name": "...", "description": "...", "parameters": {...}}]

Query:
<user question>

Answer:
[{"name": "...", "arguments": {...}}]
```

### Training Setup

| Parameter | Value |
|-----------|-------|
| Base model | `Qwen/Qwen2.5-3B-Instruct` |
| Fine-tuning library | Unsloth (2x faster) |
| Method | LoRA (PEFT) |
| LoRA rank | 16 |
| LoRA alpha | 16 |
| Target modules | q, k, v, o, gate, up, down projections |
| Quantization | 4-bit (QLoRA) |
| Batch size | 2 per device |
| Gradient accumulation | 4 steps (effective batch = 8) |
| Learning rate | 2e-4 |
| Optimizer | AdamW 8-bit |
| Epochs | 1 per run |
| Max sequence length | 2048 |
| Hardware | Tesla T4 (Kaggle) |
| Trainable parameters | 29.9M / 3.1B (0.96%) |

### Training Results

| Run | Training Samples | Steps | Training Loss | Samples/sec |
|-----|-----------------|-------|--------------|-------------|
| Run 1 | 5,000 | 625 | 0.5861 | 1.53 |
| Run 2 | 5,000 (10k total) | 625 | 0.4054 | 1.72 |

Loss dropped from **0.586 → 0.405** between runs, showing consistent improvement with more data.

### Evaluation Results

**Large-scale test — 250 samples from xlam-60k (Run 2):**

| Metric | Score |
|--------|-------|
| Total samples | 250 |
| Correct | 180 |
| Failed | 70 |
| Exact Match Accuracy | **72.0%** |

**Base model vs Fine-tuned — 6 held-out test cases:**

| Metric | Base Qwen2.5-3B | Fine-Tuned |
|--------|----------------|-----------|
| Tool Accuracy | 100% | 100% |
| Argument Accuracy | 33.3% | **100%** |
| Exact Match | 33.3% | **100%** |

The base model identifies the correct tool but fails at argument formatting — adding extra fields, using wrong key names, or generating verbose explanations instead of JSON. The fine-tuned model outputs clean, structured JSON with no additional prompting.

**Example output comparison:**

```
Query: "What's the status of order #48291?"

Base Model:
  I will get the current status of order #48291 for you...
  {"name": "get_order_status", "input": {"order_id": "48291"}}
  The order status is "Shipped". Let me know if you need anything else...

Fine-Tuned:
  [{"name": "get_order_status", "arguments": {"order_id": "48291"}}]
```

### Key Takeaways

- Argument accuracy jumped from **33% → 100%** after fine-tuning
- The model correctly refuses to call tools for out-of-scope queries (e.g. "What is the capital of France?" returns no tool call)
- Multi-tool queries work correctly (e.g. asking for stock price + company info + news in one query)
- Earlier failures caused by extra parameters or wrong argument names were resolved with more training data and better tool descriptions

### Published Model

The final merged model (16-bit) is published on Hugging Face:
[FatalHub/qwen-function-calling-10k](https://huggingface.co/FatalHub/qwen-function-calling-10k)

---

## Notebooks

| Notebook | Description |
|----------|-------------|
| `FuncCallFT.ipynb` | Full fine-tuning pipeline: data prep, LoRA setup, training, push to hub |
| `creatingtools.ipynb` | Building and testing Alpha Vantage tool implementations |
| `ft-base-comparison.ipynb` | Side-by-side evaluation of base vs fine-tuned model |
| `inference.ipynb` | Serving the model behind a FastAPI endpoint via ngrok |
| `toolcalling-testing.ipynb` | End-to-end tool calling tests with the deployed model |
