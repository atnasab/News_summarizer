# News Summarizer Project

This project fetches news from the NewsAPI, summarizes it using a Hugging Face model, stores it in MongoDB, and serves it through a Flask API. A frontend (React) or mobile app (Flutter) fetches the summarized data and displays it.

## Folder Structure
- `backend/`: Python Fast API to fetch, summarize, and serve news.
- `frontend/`: React.js frontend to display summarized news.
- `mobile/`: Placeholder for Flutter code.

## Instructions
1. Run MongoDB and replace API keys in `config/config.py`.
2. Install backend requirements:
    ```
    pip install -r backend/requirements.txt
    ```
3. Run the Flask API:
    ```
    python backend/app.py
    ```
4. Run the React frontend:
    ```
    cd frontend
    npm install
    npm start
    ```
