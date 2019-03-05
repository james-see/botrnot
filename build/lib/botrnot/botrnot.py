"""A script to grab twitter data."""
# !/usr/bin/python3
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-Jan-2018
# Last Update: 03-05-2019
# Requirements: minimal. check requirements.txt and run pip/pip3 install -f requirements.txt

# imports section
import argparse
import json
from twitter_scraper import get_tweets
from bs4 import BeautifulSoup
import requests
from beautifultable import BeautifulTable

# globals
__version__ = "1.0.7"
# ANSI color terminal escape sequences
OKBLUE = '\033[94m'
ENDC = '\033[0m'
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
PARSER = argparse.ArgumentParser(description='collects and processes twitter data example: botrnot -u jamescampbell',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('-u', '--user', dest='username',
                    help='username to evaluate', default='jamescampbell', required=False)
PARSER.add_argument('-n', '--no-logo', dest='nologo', action='store_true', default=False, help='dont display logo (default False)')
PARSER.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='print more things out about search')
PARSER.add_argument('-j', '--json', dest='jsonout', action='store_true', default=False, help='save tweets out to json file')
args = PARSER.parse_args()


# functions section


def get_content(username):
    """Get data from requests object from itunes endpoint."""
    tweets = []
    for tweet in get_tweets(username, pages=25):
        tweets.append(tweet)
    return tweets


def get_user_data(username):
    """Get user info for profile."""
    userdata = dict()
    r = requests.get(f'https://www.twitter.com/{username}')
    soup = BeautifulSoup(r.text, 'html.parser')
    following = soup.find('li', class_='ProfileNav-item--following')
    following = following.find('span', class_='ProfileNav-value')
    userdata['following'] = following.text
    followers = soup.find('li', class_='ProfileNav-item--followers')
    followers = followers.find('span', class_='ProfileNav-value')
    userdata['followers'] = followers.text
    twittername = soup.find('h1', class_='ProfileHeaderCard-name')
    userdata['fullname'] = twittername.text.strip()
    userbio = soup.find('p', class_='ProfileHeaderCard-bio')
    userdata['userbio'] = userbio.text
    userlocation = soup.find('div', class_='ProfileHeaderCard-location')
    userdata['userlocation'] = userlocation.text.strip()
    userdatejoined = soup.find('div', class_='ProfileHeaderCard-joinDate')
    userdata['userjoindate'] = userdatejoined.text.strip()
    userbirthdate = soup.find('div', class_='ProfileHeaderCard-birthdate')
    userdata['userbirthdate'] = userbirthdate.text.strip()
    if args.verbose:
        t = BeautifulTable()
        # t.column_headers = ['Item', 'Value']
        t.append_row(["Full Name:", f"{OKBLUE}{userdata['fullname']}{ENDC}"])
        t.append_row(["Followers count:", OKBLUE+userdata['followers']+ENDC])
        t.append_row(["Following count:", OKBLUE+userdata['following']+ENDC])
        t.append_row(["User Biography:", OKBLUE+userdata['userbio']+ENDC])
        t.append_row(["User Location:", OKBLUE+userdata['userlocation']+ENDC])
        t.append_row(["User Join Date:", OKBLUE+userdata['userjoindate']+ENDC])
        t.append_row(["User Birth Date:", OKBLUE+userdata['userbirthdate']+ENDC])
        print(t)
    return userdata

# main section


def main():
    """Main function that runs everything."""
    if args.nologo is not True:
        print(logo)
    userdatadict = get_user_data(args.username)
    tweetslist = get_content(args.username)
    if args.verbose:
        print(f"First tweet in list: {tweetslist[0]}")
    if args.jsonout:
        with open('{}-tweets.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(tweetslist, indent=4, sort_keys=True, default=str))
        with open('{}-profile.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(userdatadict, indent=4, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
