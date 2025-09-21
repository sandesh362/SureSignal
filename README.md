# README.md
# Misinformation Detection Pipeline

A Python pipeline for collecting and preprocessing news articles and tweets related to misinformation detection.

## Features

- **Data Collection**: Collect news articles from NewsAPI and tweets from Twitter API
- **Text Preprocessing**: Clean and normalize text data with NLP techniques
- **MongoDB Storage**: Store collected data in MongoDB
- **Error Handling**: Robust error handling and logging
- **Duplicate Prevention**: Avoid inserting duplicate articles/tweets

## Setup

1. **Install dependencies**:
   ```bash
   python setup.py
   ```

2. **Configure API keys** in `config/config.yaml`:
   - Get NewsAPI key from: https://newsapi.org/
   - Get Twitter Bearer Token from: https://developer.twitter.com/

3. **Start MongoDB** (if running locally):
   ```bash
   mongod
   ```

4. **Run the pipeline**:
   ```bash
   python main.py
   ```

## Project Structure

```
├── config/
│   └── config.yaml          # API keys and configuration
├── storage/
│   └── db.py               # MongoDB connection
├── ingestion/
│   ├── news_ingest.py      # NewsAPI data collection
│   └── twitter_ingest.py   # Twitter data collection
├── preprocessing/
│   └── clean_text.py       # Text cleaning utilities
├── tests/
│   └── test_ingestion.py   # Basic tests
├── main.py                 # Main pipeline script
├── setup.py               # Setup script
└── requirements.txt       # Dependencies
```

## Usage

The pipeline will:
1. Collect recent tweets and news articles about misinformation
2. Clean and preprocess the text data
3. Store everything in MongoDB with duplicate prevention
4. Provide progress updates and error handling

## Requirements

- Python 3.7+
- MongoDB
- Internet connection for API calls
- Valid API keys for NewsAPI and Twitter
