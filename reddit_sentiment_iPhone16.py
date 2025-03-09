import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------------- Reddit API Setup ----------------
reddit = praw.Reddit(
    client_id="XXXXXXXXXXXXXXX",
    client_secret="YYYYYYYYYYYYYYYYY",
    username="WWWWWWWWWWW",
    password="ZZZZZZZZZZZZZZZ",
    user_agent="iPhoneSentimentBot v1",

)

# ---------------- Sentiment Analyzer Setup ----------------
analyzer = SentimentIntensityAnalyzer()

# ---------------- Search Query ----------------
posts = reddit.subreddit("Smartphones").search("iPhone 16", limit=30)

# ---------------- Extract Posts + Comments ----------------
data = []

for post in posts:
    # Check if this is a "Pro" post based on title
    post_label = "iPhone 16 Pro" if "pro" in post.title.lower() else "iPhone 16"
    
    # Analyze post title sentiment
    title_sentiment = analyzer.polarity_scores(post.title)
    data.append({
        'post_or_comment': 'Post',
        'product_label': post_label,
        'content': post.title,
        'score': post.score,
        'num_comments': post.num_comments,
        'sentiment_neg': title_sentiment['neg'],
        'sentiment_pos': title_sentiment['pos'],
        'sentiment_compound': title_sentiment['compound']
    })

    # Extract and analyze each comment
    post.comments.replace_more(limit=0)
    for comment in post.comments:
        comment_label = "iPhone 16 Pro" if "pro" in comment.body.lower() else "iPhone 16"
        sentiment = analyzer.polarity_scores(comment.body)
        data.append({
            'post_or_comment': 'Comment',
            'product_label': comment_label,
            'content': comment.body,
            'score': comment.score,
            'num_comments': None,
            'sentiment_neg': sentiment['neg'],
            'sentiment_pos': sentiment['pos'],
            'sentiment_compound': sentiment['compound']
        })

# ---------------- Save to CSV ----------------
df = pd.DataFrame(data)
df.to_csv("reddit_posts_comments_sentiment_iphone16.csv", index=False)
print("iPhone 16 and iPhone 16 Pro sentiment data saved to 'reddit_posts_comments_sentiment_iphone16.csv'")

