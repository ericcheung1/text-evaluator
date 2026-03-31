import praw
from praw.exceptions import RedditAPIException, InvalidURL
import os

def authenticate_reddit():
    """
    Authenticates a reddit instance in PRAW.

    Authenticates a reddit instance using 
    information and keys from a .env file.
    """
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    reddit_instance = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="test_bot"
    )
    # TODO: in authenticate_reddit() add error handling 
    # to failed reddit connections
    print(f'Logged in as user: {reddit_instance.user.me()}')
    return reddit_instance

def get_comments(reddit_instance, url):
    """
    """
    
    try:
        submission = reddit_instance.submission(url=url)
    except InvalidURL:
        return {"Error": "Invalid URL"}
    except RedditAPIException:
        return {"Error": "Reddit API"}

    submission.comments.replace_more(limit=5)
    comment_queue = submission.comments[:5]

    count = 0
    comments = []

    while comment_queue:
        comment = comment_queue.pop(0)
        comments.append({
            "user_id": str(comment.author.id),
            "comment_id": str(comment.id),
            "comment": str(comment.body),
        })
        count+=1
        if count >= 5:
            break
        comment_queue.extend(comment.replies)

    return comments

def connect_sentiment():
    """
    """

    sentiment_url = os.getenv("url_prod")
    
    if sentiment_url is None:
        return "error: failed to load api url"
    else:
        return sentiment_url

if __name__ == "__main__":
    from dotenv import load_dotenv
    import json

    load_dotenv()
    reddit = authenticate_reddit()
    url = ""
    
    comments = get_comments(reddit, url)
    print(json.dumps(comments, indent=4))
    with open("data.json", "w") as file:
        json.dump(comments, file, indent=4)
