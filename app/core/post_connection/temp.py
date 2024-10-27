import praw
import os
from dotenv import load_dotenv

load_dotenv(override=True)

import os
print(os.getenv("REDDIT_CLIENT_ID"))
print(os.getenv("REDDIT_SECRET_KEY"))
print(os.getenv("REDDIT_USER_AGENT"))


reddit = praw.Reddit(
    client_id="G-gQxH-DjG3HbEwj2ZKYYA",
    client_secret="fUHGvJKgWJNgcSZDtd4v1zm4Iv3mUQ",
    user_agent="desktop:test_script:v1.0 (by /u/Upbeat-War2890)"
)
reddit.read_only = True



print(reddit.subreddit("learnpython").title)  # Should return "learnpython"