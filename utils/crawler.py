import os
import sys
from pathlib import Path

import django

import time
from datetime import datetime

import praw
import requests
from bs4 import BeautifulSoup
import pytz
from django.conf import settings


# popular
# default


# def random_subreddits():
#     subreddits = []
#     for _ in range(100):
#         subreddit = reddit.random_subreddit()
#         print(subreddit.display_name)
#         print(subreddit.banner_img)
#         print(subreddit.subscribers)
#         print(subreddit.created_utc)
#         print(subreddit.url)
#         print(subreddit.public_description)
#         print("-" * 55)
#         subreddits.append(subreddit)
#         time.sleep(1)

#     print(subreddits)


def get_subreddits():
    CLIENT_ID = settings.REDDIT_CLIENT_ID
    SECRET_KEY = settings.REDDIT_SECRET_KEY
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36"
    params = {
        "grant_type": "password",
        "username": settings.REDDIT_USERNAME,
        "password": settings.REDDIT_PASSWORD,
    }

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=SECRET_KEY,
        user_agent=USER_AGENT,
        username="theognis1002",
        password="Dagger10!",
    )

    for subreddit in reddit.subreddits.default():
        creation_date = datetime.utcfromtimestamp(int(subreddit.created_utc))
        creation_date = pytz.utc.localize(creation_date)

        sub, created = Subreddit.objects.get_or_create(
            name=subreddit.display_name,
            description=subreddit.public_description,
            url=subreddit.url,
            banner_img=subreddit.banner_img,
            creation_date=creation_date,
        )

        sub_history, previous_record = SubscriberHistory.objects.get_or_create(
            subreddit=sub, current_count=subreddit.subscribers
        )
        if not previous_record:
            sub_history.previous_count = sub_history.current_count
            sub_history.save()

        if created:
            print(f"{subreddit.display_name} added!")
        else:
            print(f"Duplicate: {subreddit.display_name}")


subreddits = []


# def crawl_reddistlist(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "lxml")
#     listing_row = soup.find_all("div", {"class": "listing-item"})
#     for row in listing_row:
#         anchor_tag = row.find("a")
#         subreddit_name = row.find("a").text
#         url = row.find("a")["href"].split(".com")[1]
#         # print(subreddit_name)
#         subreddits.append(subreddit_name)

#     next_page = soup.find("li", {"id": "next-page"})
#     if next_page:
#         next_page_url = next_page.find("a")["href"]
#         if "disabled" not in next_page["class"]:
#             crawl_reddistlist(next_page_url)


def main():
    # crawl_reddistlist("http://redditlist.com/all")
    # print(list(set(subreddits)))
    # print(len(subreddits))
    get_subreddits()


if __name__ == "__main__":
    BASE_DIR = str(Path(__file__).resolve().parent.parent)
    sys.path.append(BASE_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reddit_stats.settings")
    django.setup()
    from content.models import Subreddit, SubscriberHistory

    main()