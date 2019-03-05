"""A script to grab twitter data."""
# !/usr/bin/python3
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-Jan-2018
# Last Update: 03-05-2019
# Requirements: minimal. check requirements.txt and run pip/pip3 install -f requirements.txt

# imports section
import argparse
from twitter_scraper import get_tweets
import json

# globals
__version__ = "1.0.2"
logo = """
┌───────────────────────────┐
│      Bot R Not            |
│    ____                   |
|   /  __\          ____    |                
|   \( oo          (___ \   |                  
|   _\_o/           oo~)/   |
|  / \|/ \         _\-_/_   |
| / / __\ \___    / \|/  \  |
| \ \|   |__/_)  / / .- \ \ |
|  \/_)  |       \ \ .  /_/ |
|   ||___|        \/___(_/  |
|   | | |          | |  |   |
|   | | |          | |  |   |
|   |_|_|          |_|__|   |
|   [__)_)        (_(___]   |
|                           |
└───────────────────────────┘
"""

# arguments
parser = argparse.ArgumentParser(description='collects and processes twitter data example: botrnot -u jamescampbell',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-u', '--user', dest='username',
                    help='username to evaluate', default='jamescampbell', required=False)
parser.add_argument('-n', '--no-logo', dest='nologo', action='store_true', default=False, help='dont display logo (default False)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='print more things out about search')
parser.add_argument('-j', '--json', dest='jsonout', action='store_true', default=False, help='save tweets out to json file')
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
    if args.nologo != True:
        print(logo)
    tweetslist = get_content(args.username)
    if args.verbose:
        print(f"First tweet in list: {tweetslist[0]}")
    if args.jsonout:
        with open('{}-tweets.json'.format(args.username),'w+') as f:
            f.write(json.dumps(tweetslist,indent=4, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
