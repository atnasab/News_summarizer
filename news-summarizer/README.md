# News Summarizer Project

This project fetches news from the NewsAPI, summarizes it using a Hugging Face model, stores it in MongoDB, and serves it through a Flask API. A frontend (React) or mobile app (Flutter) fetches the summarized data and displays it.

## Folder Structure
- `backend/`: Python Flast API to fetch, summarize, and serve news.
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


news-summarizer/
│
├── src/
│   ├── scraper/
│   │   ├── newspaper_scraper.py          # Uses newspaper3k for supported sites
│   │   ├── custom_scraper/               # Custom scripts for Nepalese sites
│   │   │   ├── base_scraper.cs           # Base scraper class for .NET
│   │   │   ├── nepal_scraper.cs          # Custom scraper for Nepalese sites
│   │   │   └── helpers/
│   │   │       ├── utils.cs              # Helper methods for scraping
│   │   │       └── parsers.cs            # Parsing helpers for different formats
│   │   └── tests/
│   │       ├── test_newspaper_scraper.py # Unit tests for newspaper scraper
│   │       ├── test_custom_scraper.cs    # Unit tests for custom scraper
│   │       └── mock_data/                # Mock HTML data for testing
│   │           └── sample_site.html
│   │
│   ├── summarizer/
│   │   ├── summarizer.py                 # Python-based summarization logic
│   │   └── tests/
│   │       └── test_summarizer.py        # Unit tests for summarizer
│   │
│   ├── api/
│   │   ├── main.py                       # FastAPI for backend API
│   │   ├── routes/
│   │   │   ├── news_routes.py            # Routes for fetching news
│   │   │   └── summarization_routes.py   # Routes for summarization
│   │   └── tests/
│   │       └── test_api.py               # Unit tests for API
│   │
│   └── frontend/
│       ├── public/                       # Static assets
│       ├── src/
│       │   ├── App.js                    # React/Angular/Vue main component
│       │   ├── components/               # Reusable components
│       │   ├── services/
│       │   │   ├── api.js                # API service for fetching data
│       │   │   └── utils.js              # Utility functions for the frontend
│       │   └── styles/                   # CSS or SCSS files
│       └── tests/
│           └── test_frontend.js          # Frontend tests
│
├── data/
│   ├── raw/                              # Raw scraped data for analysis
│   ├── processed/                        # Processed data ready for summarization
│   └── logs/
│       ├── scraper_logs.log              # Logs for scraper
│       └── summarizer_logs.log           # Logs for summarizer
│
├── configs/
│   ├── docker/
│   │   ├── Dockerfile                    # Dockerfile for the project
│   │   ├── docker-compose.yml            # Docker Compose for multi-container setup
│   │   └── README.md                     # Instructions for Docker usage
│   ├── server_config.json                # Server configurations
│   ├── db_config.json                    # MongoDB connection details
│   └── logging_config.json               # Config for logging system
│
├── docs/
│   ├── README.md                         # Project overview and instructions
│   ├── CONTRIBUTING.md                   # Guidelines for contributors
│   └── API_DOC.md                        # API documentation
│
├── .gitignore                            # Ignored files/folders for Git
├── requirements.txt                      # Python dependencies
├── package.json                          # Frontend dependencies
├── docker-compose.yml                    # Root Docker Compose file
└── LICENSE                               # License for the project
           

