import praw
import pandas as pd
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------------- Reddit API Setup ----------------
reddit = praw.Reddit(
    client_id="FAzVv*******byNvgw",
    client_secret="nRP******qwEfFJsA42Q",
    username="Sea-Roo******",
    password="*************",
    user_agent="SamsungSentimentBot v1"
)

# ---------------- Sentiment Analyzer Setup ----------------
analyzer = SentimentIntensityAnalyzer()

# ---------------- Search Query ----------------
posts = reddit.subreddit("Samsung").search("Samsung S25", limit=40)

# ---------------- Extract Posts + Comments ----------------
data = []

for post in posts:
    # Check if this is an "Ultra" post based on title
    post_label = "S25 Ultra" if "ultra" in post.title.lower() else "S25"

    # Analyze post title sentiment
    title_sentiment = analyzer.polarity_scores(post.title)
    post_date = datetime.fromtimestamp(post.created_utc).date()
    
    data.append({
        'post_or_comment': 'Post',
        'product_label': post_label,
        'content': post.title,
        'score': post.score,
        'num_comments': post.num_comments,
        'created_date': post_date,
        'sentiment_neg': title_sentiment['neg'],
        'sentiment_pos': title_sentiment['pos'],
        'sentiment_compound': title_sentiment['compound']
    })

    # Extract and analyze each comment
    post.comments.replace_more(limit=0)  # remove "load more comments"
    for comment in post.comments:
        comment_label = "S25 Ultra" if "ultra" in comment.body.lower() else "S25"
        sentiment = analyzer.polarity_scores(comment.body)
        comment_date = datetime.fromtimestamp(comment.created_utc).date()
        
        data.append({
            'post_or_comment': 'Comment',
            'product_label': comment_label,
            'content': comment.body,
            'score': comment.score,
            'num_comments': None,
            'created_date': comment_date,
            'sentiment_neg': sentiment['neg'],
            'sentiment_pos': sentiment['pos'],
            'sentiment_compound': sentiment['compound']
        })

# ---------------- Save to CSV ----------------
df = pd.DataFrame(data)
df.to_csv("reddit_sentiment_s25_and_ultra.csv", index=False)
print("Sentiment data saved to 'reddit_sentiment_s25_and_ultra.csv'")

