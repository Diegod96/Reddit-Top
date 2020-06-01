import time
import datetime as dt
import random

from config import initialize_reddit_app
from constants import SUBREDDITS


def clean_submission(submission):
    now_iso = dt.datetime.utcnow().isoformat()
    created_iso = dt.datetime.utcfromtimestamp(submission.created_utc).isoformat()

    try:
        submission_author = submission.author.name
    except:
        submission_author = "None"
    data = {
        "id": submission.id,
        "title": submission.title,
        "score": submission.score,
        "url": submission.url,
        "name": submission.name,
        "author": submission_author,
        "is_video": submission.is_video,
        "over_18": submission.over_18,
        "selftext": submission.selftext,
        "shortlink": submission.shortlink,
        "subreddit_type": submission.subreddit_type,
        "subreddit_subscribers": submission.subreddit_subscribers,
        "thumbnail": submission.thumbnail,
        "ups": submission.ups,
        "created_utc": created_iso,
        "archived": now_iso
    }

    for k, v in data.items():
        if v == "":
            data[k] = "None"
    return data


def hot_submissions(sub, min_upvotes):
    data = []
    red = initialize_reddit_app()
    subreddit = red.subreddit(sub)
    submissions = subreddit.hot()

    for submission in submissions:
        if submission.ups > min_upvotes:
            article = clean_submission(submission)
            article['subreddit'] = sub
            data.append(article)
    return data


def lambda_handler(event, context):
    random_subreddit = SUBREDDITS[random.randint(0, len(SUBREDDITS) - 1)]
    data = hot_submissions(random_subreddit, 500)
    data.sort(key=lambda x: x['ups'])
    return data


if __name__ == '__main__':
    data = lambda_handler(None, None)
    for x in data:
        print(x['title'])
        for item in ['ups', 'subreddit', 'created_utc', 'selftext', 'author']:
            print('{}: {}'.format(item, x[item]))
        print("_" * 50)
