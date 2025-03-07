import praw
import logging
from transformers import pipeline

# Configure logging (optional, but good for debugging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)
logger = logging.getLogger(__name__)

def get_reddit_comment_texts(subreddit_name, submission_id, client_id, client_secret, user_agent):
    """
    Collect ALL comment texts from a specific Reddit submission using PRAW.
    This function is designed to retrieve all comments, including nested replies,
    by using `submission.comments.replace_more(limit=0)`.

    Args:
        subreddit_name (str): The name of the subreddit (e.g., "technology").
        submission_id (str): The ID of the Reddit submission (e.g., "18mayday").
        client_id (str): Your Reddit API client ID.
        client_secret (str): Your Reddit API client secret.
        user_agent (str): A descriptive user agent string for your application.

    Returns:
        list: A list of strings, where each string is the text content of a comment.
              Returns an empty list if there's an error or no comments are found.
              In theory, this should return ALL comments, but extremely large
              comment sections might have practical limitations due to API behavior
              or time constraints.
    """
    logger.info(f"Collecting ALL comment texts from submission {submission_id} in r/{subreddit_name}")

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

        submission = reddit.submission(id=submission_id)

        comment_texts = []

        # Replace "MoreComments" objects to load ALL comments, including nested replies.
        # limit=0 means replace all "MoreComments" instances.
        submission.comments.replace_more(limit=0)

        # Iterate through ALL comments in the submission's comment forest.
        # After replace_more(limit=0), submission.comments.list() should contain
        # a flat list of all comment objects.
        for comment in submission.comments.list():
            if hasattr(comment, 'body'):  # Check if it's a comment object with a body
                comment_texts.append(comment.body)  # Just append the comment text

        logger.info(f"Collected {len(comment_texts)} comment texts (attempted to get ALL)")
        return comment_texts

    except Exception as e:
        logger.error(f"Error collecting Reddit comment texts (attempting to get ALL): {str(e)}")
        return []

def analyze_sentiment_transformers(comment_texts):
    """
    Analyzes the sentiment of a list of comment texts using Hugging Face Transformers pipeline.
    (No changes here, sentiment analysis part remains the same)
    """
    logger.info("Analyzing sentiment of comment texts using Transformers pipeline")

    sentiment_pipeline = pipeline("sentiment-analysis") # Initialize sentiment analysis pipeline

    sentiment_results = []
    for text in comment_texts:
        try:
            result = sentiment_pipeline(text)[0] # Get sentiment for the text
            sentiment_results.append({
                "comment_text": text,
                "sentiment_label": result['label'],
                "sentiment_score": result['score']
            })
        except Exception as e:
            logger.error(f"Error analyzing sentiment for comment: '{text[:50]}...': {e}") # Log error, limit text length
            sentiment_results.append({
                "comment_text": text,
                "sentiment_label": "Error",
                "sentiment_score": None,
                "error_message": str(e)
            }) # Add error info to result

    logger.info(f"Sentiment analysis completed for {len(sentiment_results)} comments")
    return sentiment_results


if __name__ == '__main__':
    # --- Replace these with your actual Reddit API credentials and target submission ---
    REDDIT_CLIENT_ID = "your_clientid"  # Replace with your client ID
    REDDIT_CLIENT_SECRET = "Secret_key" # Replace with your client secret
    REDDIT_USER_AGENT = "CommentSentimentAnalyzerBot by /u/deekshith_n_shetty" # Replace with your user agent
    SUBREDDIT_NAME = "movies"  # Example subreddit you can take any example discussion
    SUBMISSION_ID = "1j5e3f7"   # Example submission ID

    if REDDIT_CLIENT_ID == "YOUR_CLIENT_ID" or REDDIT_CLIENT_SECRET == "YOUR_CLIENT_SECRET" or REDDIT_USER_AGENT == "CommentSentimentAnalyzerBot by /u/YOUR_REDDIT_USERNAME":
        logger.error("Please replace the placeholder Reddit API credentials and user agent in the __main__ block.")
    else:
        comment_texts = get_reddit_comment_texts(
            SUBREDDIT_NAME,
            SUBMISSION_ID,
            REDDIT_CLIENT_ID,
            REDDIT_CLIENT_SECRET,
            REDDIT_USER_AGENT
        )

        if comment_texts:
            print(f"Successfully fetched {len(comment_texts)} comment texts from r/{SUBREDDIT_NAME}, submission ID: {SUBMISSION_ID} (attempted to get ALL)")

            sentiment_analysis_results = analyze_sentiment_transformers(comment_texts)

           # Replace the existing results display section in the __main__ block with this:
if sentiment_analysis_results:
    print(f"\n--- Sentiment Analysis Results (All {len(sentiment_analysis_results)} Comments) ---")
    for i, result in enumerate(sentiment_analysis_results):
        print(f"\nComment {i+1}: '{result['comment_text'][:50]}...'")  # Print snippet of comment
        print(f"  Sentiment: {result['sentiment_label']}")
        print(f"  Score: {result['sentiment_score']:.4f}")  # Format score to 4 decimal places
        if 'error_message' in result:
            print(f"  Error: {result['error_message']}")
else:
    print("Sentiment analysis failed or returned no results.")
