# Smart Shopping Agent — Real-Time E-Commerce Data

An end-to-end implementation of the Smart Shopping Agent described in the supplied Hexaware presentation.

## What is implemented

**Flow:** Natural-language query → intent extraction → live product search → normalization/filtering → FAISS relevance retrieval → multi-factor ranking → LLM explanation → comparison UI → SQLite history.

The project keeps the presentation's core technologies: **Python, Streamlit, Ollama, LangChain-compatible architecture, FAISS, BeautifulSoup and SQLite**, while using **SerpApi Google Shopping** as the live product-search provider.

> Live shopping results require a SerpApi API key. Product prices, availability and ratings are time-varying and should be treated as a snapshot obtained at search time.

## Architecture

```text
                         +----------------------+
 User query ----------> | Streamlit UI         |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Intent Extractor     |
                         | Ollama / fallback    |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Live Search Provider |
                         | SerpApi Shopping     |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Normalizer / Cleaner |
                         | BeautifulSoup utils  |
                         +----------+-----------+
                                    |
                  +-----------------+------------------+
                  |                                    |
                  v                                    v
        +----------------------+             +----------------------+
        | SQLite search/cache  |             | FAISS relevance      |
        | audit/history        |             | retrieval            |
        +----------------------+             +----------+-----------+
                                                       |
                                                       v
                                             +----------------------+
                                             | Ranking Engine       |
                                             | relevance + price    |
                                             | rating + reviews     |
                                             | feature match        |
                                             +----------+-----------+
                                                        |
                                                        v
                                             +----------------------+
                                             | Ollama explanation   |
                                             | pros / cons / fit    |
                                             +----------+-----------+
                                                        |
                                                        v
                                             +----------------------+
                                             | Streamlit comparison |
                                             +----------------------+
```

## Requirements

- Python 3.11+
- SerpApi account/API key
- Ollama installed locally (optional; the application has a deterministic fallback if Ollama is unavailable)
- Internet access

## Setup in VS Code

### 1. Create and activate a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure secrets

Copy `.env.example` to `.env`:

```bash
SERPAPI_API_KEY=your_serpapi_key
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
CACHE_TTL_SECONDS=300
```

Do not commit `.env`.

### 4. Start Ollama (optional but recommended)

```bash
ollama pull llama3.2:3b
ollama serve
```

If you do not run Ollama, the intent extractor and explanation engine automatically use deterministic Python fallbacks.

### 5. Run

```bash
streamlit run app/main.py
```

Then open the URL shown by Streamlit.

## Example queries

- `Find a laptop under ₹80,000 for Power BI, Python and office work`
- `Best noise cancelling headphones under ₹20,000 for travel`
- `I need running shoes under ₹8,000 for daily road running`
- `Buy a 55 inch 4K TV under ₹60,000 with good reviews`

The UI also exposes explicit category, budget, rating and result-count filters.

## Live-data design

The app calls:

`https://serpapi.com/search?engine=google_shopping`

with the user's query and location. The API documentation states that `q` is the shopping search query and that the endpoint returns Google Shopping results. See the SerpApi documentation: https://serpapi.com/google-shopping-api

The app uses a short TTL cache to avoid repeated identical API calls during Streamlit reruns. Streamlit's documentation recommends `st.cache_data` for data returned from APIs and other serializable results.

## Ranking formula

After hard budget filtering, each product receives:

```text
final_score =
    0.40 * semantic_relevance
  + 0.20 * feature_match
  + 0.15 * rating_score
  + 0.10 * review_score
  + 0.15 * price_value
```

All component scores are normalized to 0–1. The weights are configuration values, not an LLM opinion. You can change them in `app/services/ranker.py`.

## Test cases mapped to the presentation

TC01 Budget Search
TC02 Category Search
TC03 Product Search
TC04 Product Comparison
TC05 Product Recommendation
TC06 Empty Search
TC07 Invalid Product
TC08 No Product Within Budget
TC09 Invalid Filter
TC10 Missing Information

Run:

```bash
pytest -q
```

## Project structure

```text
smart_shopping_agent/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── services/
│   │   ├── search_provider.py
│   │   ├── intent.py
│   │   ├── ranker.py
│   │   ├── recommender.py
│   │   ├── llm.py
│   │   ├── vector_store.py
│   │   ├── database.py
│   │   └── text_utils.py
│   └── ui/
│       └── components.py
├── tests/
├── docs/
├── data/
├── .streamlit/
├── .env.example
├── requirements.txt
└── README.md
```

## Production hardening

For enterprise deployment, add:
- secret management (Azure Key Vault or equivalent)
- request/user authentication
- API rate-limit handling and retry/backoff
- provider health monitoring
- retailer/source normalization
- price/availability timestamps
- product deduplication using GTIN/brand/model where available
- persistent vector index
- Redis/distributed cache
- observability and PII-safe audit logs
- human review for affiliate/commercial disclosure requirements

