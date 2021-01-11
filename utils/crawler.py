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
from django.db.models import F


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
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_SECRET_KEY,
        user_agent=settings.USER_AGENT,
        username=settings.REDDIT_USERNAME,
        password=settings.REDDIT_PASSWORD,
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

        last_record = SubscriberHistory.objects.filter(subreddit=sub).last()
        time_since_last_check = (
            timezone.now() - last_record.date_recorded
        ).seconds // 3600

        if time_since_last_check > 20:
            print(f"{subreddit.display_name} subscriber count updated")
            sub_metadata = SubscriberHistory.objects.create(
                subreddit=sub, subscriber_count=subreddit.subscribers
            )

        if created:
            print(f"{subreddit.display_name} added!")


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


def update_subscriber_count():
    subreddits = (
        Subreddit.objects.annotate(
            date=F("subscriberhistory__date_recorded"),
            subscribers=F("subscriberhistory__subscriber_count"),
        )
        .order_by("id", "-date")
        .distinct()
    )
    #        filter(
    # subscriberhistory__date_recorded__lt=timezone.now() - timedelta(hours=3)

    print(subreddits)
    for sub in subreddits:
        print(sub.name, sub.date, sub.subscribers)
    exit()
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_SECRET_KEY,
        user_agent=settings.USER_AGENT,
        username=settings.REDDIT_USERNAME,
        password=settings.REDDIT_PASSWORD,
    )

    for subreddit in subreddits:
        new_subscriber_count = reddit.subreddits.search_by_name(
            subreddit.name, exact=True
        )[0].subscribers

        last_record = SubscriberHistory.objects.filter(subreddit=subreddit).last()
        time_since_last_check = (
            timezone.now() - last_record.date_recorded
        ).seconds // 3600
        print(time_since_last_check)
        if time_since_last_check > 20:
            print(f"{subreddit.display_name} subscriber count updated")
            sub_metadata = SubscriberHistory.objects.create(
                subreddit=subreddit, subscriber_count=subreddit.subscribers
            )

        time.sleep(1)


def cleanup():
    past_records = SubscriberHistory.objects.filter(
        date_recorded__lt=timezone.now() - timedelta(days=7)
    )
    past_records.delete()


def main():
    # crawl_reddistlist("http://redditlist.com/all")
    # print(list(set(subreddits)))
    # print(len(subreddits))
    # get_subreddits()
    update_subscriber_count()
    # cleanup()


if __name__ == "__main__":
    BASE_DIR = str(Path(__file__).resolve().parent.parent)
    sys.path.append(BASE_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reddit_stats.settings")
    django.setup()
    from content.models import Subreddit, SubscriberHistory
    from django.utils import timezone
    from datetime import timedelta

    main()