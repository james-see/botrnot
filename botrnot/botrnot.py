"""A script to grab twitter data."""
# !/usr/bin/python3
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-Jan-2018
# Last Update: 03-03-2019
# Requirements: minimal. check requirements.txt and run pip/pip3 install -f requirements.txt

# imports section
import argparse
from twitter_scraper import get_tweets

# globals
__version__ = "1.0.0"
logo = """
┌──────────────────────┐
│      Bot R Not       │
│                      │
└──────────────────────┘
"""

# arguments
parser = argparse.ArgumentParser(description='collects and processes twitter data example: botrnot -u jamescampbell',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-u', '--user', dest='username',
                    help='username to evaluate', default='jamescampbell', required=False)

args = parser.parse_args()


# functions section


def get_content(username):
    """Get data from requests object from itunes endpoint."""
    tweets = []
    for tweet in get_tweets(username, pages=25):
        tweets.append(tweet)
        return tweets

# main section


def main():
    """Main function that runs everything."""
    tweetslist = get_content(args.username)
    print(tweetslist[0])


if __name__ == "__main__":
    main()
