# AI Sales Analytics Agent

A Streamlit app that turns natural-language sales questions into SQLite queries,
then summarizes the results with Gemini.

## Configuration

Set `GEMINI_API_KEY` to a Gemini API key. The app loads it from the process
environment or a local `.env` file. Optionally set `GEMINI_MODEL` to select a
Gemini model; the default is `gemini-3.8-flash`.

Never commit your API key. `.env` is ignored by Git.

## Deploy to Render

Create a **Web Service** for this repository and configure:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`
- **Environment variable:** `GEMINI_API_KEY` = your Gemini API key
- **Optional environment variable:** `GEMINI_MODEL` = a model available to your API key

The sample SQLite database is stored in `data/sales.db` and must be included in
the repository. Render's standard filesystem is ephemeral, so use persistent
storage or a managed database if database changes need to survive redeployments.

## Run locally

Install dependencies with `pip install -r requirements.txt`, set `GEMINI_API_KEY`
in your environment or `.env` file, then run `streamlit run app.py`.