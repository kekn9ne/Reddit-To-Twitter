from config import username, password, headless, client_id, client_secret, user_agent, post_type, subreddits, wait_before_posting
from twitter import Twitter
import time
import praw
import os
import random
import urllib.request

twitter = Twitter(username, password, headless)
twitter.signIn()

def bot_login():
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    return reddit

def bot_run(reddit, blacklist):
    subreddit = random.choice(subreddits)
    if post_type == "hot":
        submission = reddit.subreddit(subreddit).hot(limit=10)
    elif post_type == "top":
        submission = reddit.subreddit(subreddit).top(limit=10)
    elif post_type == "new":
        submission = reddit.subreddit(subreddit).new(limit=10)
    elif post_type == "rising":
        submission = reddit.subreddit(subreddit).rising(limit=10)
    else: 
        return print("Unknown post type. Edit post_type in config file.")

    for submission in submission:
        if submission.id not in blacklist and (not submission.over_18 and (submission.url.endswith("jpg") or submission.url.endswith("jpeg") or submission.url.endswith("png"))):
            print("Image found. Downloading.")

            urllib.request.urlretrieve(submission.url, submission.id + ".png")
            
            print("Image Downloaded. Tweeting.")
            title = submission.title

            if len(title) > 280:
                title = title[0:277] + "..."

            twitter.tweet(title, os.path.abspath(submission.id + ".png"))

            blacklist.append(submission.id)
            with open("./blacklist.txt", "a") as f:
                f.write(submission.id + "\n")

            try:
                os.remove(submission.id + ".png")
            except:
                return

            return
        else:
            continue

def get_blacklist():
    if not os.path.isfile("./blacklist.txt"):
            blacklist = []
    else:
        with open("./blacklist.txt", "r") as f:
            blacklist = f.read().split("\n")
    
    return blacklist

reddit = bot_login()
blacklist = get_blacklist()

while True:
    bot_run(reddit, blacklist)
    time.sleep(wait_before_posting)