# Reddit Sentiment Analyzer

## Description

Reddit Sentiment Analyzer is a Python-based project that retrieves comments from a specific Reddit submission and analyzes their sentiment using Hugging Face Transformers' sentiment-analysis pipeline. The script provides insights into whether the comments are positive, negative, or neutral.

## Features

- Fetches all comments from a Reddit submission, including nested replies.
- Uses the Hugging Face Transformers library for sentiment analysis.
- Logs progress and errors using Python's logging module.
- Displays sentiment results with confidence scores.

## Requirements

- Python 3.x
- `praw` (Python Reddit API Wrapper)
- `transformers` (Hugging Face NLP Library)
- `torch` (for model support in Transformers)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/reddit-sentiment-analyzer.git
  
   ```
2. Install dependencies:
   ```sh
   pip install praw transformers torch
   ```

## Usage

1. Obtain Reddit API credentials from [Reddit Apps](https://www.reddit.com/prefs/apps).
2. Replace the following placeholders in `main.py` with your actual credentials:
   ```python
   REDDIT_CLIENT_ID = "your_client_id"
   REDDIT_CLIENT_SECRET = "your_client_secret"
   REDDIT_USER_AGENT = "your_user_agent"
   ```
3. Run the script:
   ```sh
   python main.py
   ```
4. The script will retrieve comments from the specified submission and analyze their sentiment, displaying the results in the terminal.

## Example Output

```
Successfully fetched 20 comment texts from r/movies, submission ID: 1j5e3f7

--- Sentiment Analysis Results ---
Comment 1: 'This movie was absolutely fantastic! Loved it! ...'
  Sentiment: POSITIVE
  Score: 0.98

Comment 2: 'I didn't enjoy this one. The pacing was too slow...'
  Sentiment: NEGATIVE
  Score: 0.85
```


## Author

ndeekshith

