import time
from datetime import datetime

import praw
import requests
from bs4 import BeautifulSoup


CLIENT_ID = "T4N3e6Q-oA1ZDg"
SECRET_KEY = "A3PRvyuYX8gBdfCYznhWLx_5dEc"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36"
params = {
    "grant_type": "password",
    "username": "theognis1002",
    "password": "Dagger10!",
}


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_KEY,
    user_agent=USER_AGENT,
    username="theognis1002",
    password="Dagger10!",
)

# popular
# default


def random_subreddits():
    subreddits = []
    for _ in range(100):
        subreddit = reddit.random_subreddit()
        print(subreddit.display_name)
        print(subreddit.banner_img)
        print(subreddit.subscribers)
        print(subreddit.created_utc)
        print(subreddit.url)
        print(subreddit.public_description)
        print("-" * 55)
        subreddits.append(subreddit)
        time.sleep(1)

    print(subreddits)


def get_subreddits():
    for subreddit in reddit.subreddits.default():
        print(subreddit.display_name)
        print(subreddit.url)
        print(subreddit.banner_img)
        print(subreddit.subscribers)
        created_date = datetime.utcfromtimestamp(int(subreddit.created_utc)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        print(created_date)
        print(subreddit.public_description)
        print("-" * 55)


subreddits = []


def crawl_reddistlist(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    listing_row = soup.find_all("div", {"class": "listing-item"})
    for row in listing_row:
        anchor_tag = row.find("a")
        subreddit_name = row.find("a").text
        url = row.find("a")["href"].split(".com")[1]
        # print(subreddit_name)
        subreddits.append(subreddit_name)

    next_page = soup.find("li", {"id": "next-page"})
    if next_page:
        next_page_url = next_page.find("a")["href"]
        if "disabled" not in next_page["class"]:
            crawl_reddistlist(next_page_url)


if __name__ == "__main__":
    # get_subreddits()
    crawl_reddistlist("http://redditlist.com/all")
    print(list(set(subreddits)))
    print(len(subreddits))