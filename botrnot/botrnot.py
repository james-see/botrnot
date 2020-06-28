"""A script to grab social media data data."""
# !/usr/bin/python3
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-Jan-2018
# Last Update: 29-JUN-2020
# Requirements: minimal. check requirements.txt and run pip/pip3 install -f requirements.txt
# imports section
import argparse
import json
from bs4 import BeautifulSoup
import requests
from beautifultable import BeautifulTable
from followers import get_followers
try:
    from __version__ import __version__
except:
    from findpi.__version__ import __version__

# globals
OKBLUE = '\033[94m'
ENDC = '\033[0m'
logo = """
┌───────────────────────────┐
│     Bot R Not   2019      |
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
                    help='username to evaluate', default='jamescampbell', required=True)
PARSER.add_argument('-n', '--no-logo', dest='nologo', action='store_true',
                    default=False, help='dont display logo (default False)')
PARSER.add_argument('--verbose', dest='verbose', action='store_true',
                    default=False, help='print more things out about search')
PARSER.add_argument('-j', '--json', dest='jsonout', action='store_true',
                    default=False, help='save tweets out to json file')
PARSER.add_argument('-f', dest='getff', action='store_true',
                    default=False, help='get followers and following data as well')
PARSER.add_argument('-v', '--version', action='version', version=__version__)
args = PARSER.parse_args()


# functions section


def get_user_data(username):
    """Get user info for profile."""
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{username}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.3 Safari/603.3.8',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    userdata = dict()
    r = requests.get(f'https://www.twitter.com/{username}', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    inputvalue = soup.find('input', class_='json-data')
    stringer = str(inputvalue)  # PITA twitter bs hidden value shit
    try:
        userdata['listed'] = stringer.split('listed_count":')[1].split(',')[0]
    except:
        userdata['listed'] = 'not listed'
    try:
        userdata['detailedcreated'] = stringer.split('created_at":"')[
            1].split(',')[0][:-1]
    except:
        userdata['detailedcreated'] = "NA"
    try:
        following = soup.find('li', class_='ProfileNav-item--following')
        following = following.find('span', class_='ProfileNav-value')
        userdata['following'] = following.text
    except:
        userdata['following'] = "NA"
    try:
        followers = soup.find('li', class_='ProfileNav-item--followers')
        followers = followers.find('span', class_='ProfileNav-value')
        userdata['followers'] = followers.text
    except:
        userdata['followers'] = "NA"
    try:
        twittername = soup.find('h1', class_='ProfileHeaderCard-name')
        userdata['fullname'] = twittername.text
        if "Verified" in twittername.text:
            userdata['fullname'] = twittername.text.split('Verified')[0]
    except:
        userdata['fullname'] = "NA"
    try:
        userbio = soup.find('p', class_='ProfileHeaderCard-bio')
        userdata['userbio'] = userbio.text
    except:
        userdata['userbio'] = "NA"
    try:
        userlocation = soup.find('div', class_='ProfileHeaderCard-location')
        userdata['userlocation'] = userlocation.text.strip()
    except:
        userdata['userlocation'] = "NA"
    try:
        userdatejoined = soup.find('div', class_='ProfileHeaderCard-joinDate')
        userdata['userjoindate'] = userdatejoined.text.strip()
    except:
        userdata['userjoindate'] = "NA"
    try:
        userbirthdate = soup.find('div', class_='ProfileHeaderCard-birthdate')
        userdata['userbirthdate'] = userbirthdate.text.strip()
    except:
        userdata['userbirthdate'] = "NA"
    try:
        userdata['userid'] = soup.find('div', class_="tweet")['data-user-id']
    except:
        userdata['userid'] = stringer.split('profile_id":')[1].split(',')[0]
    try:
        userdata['total_tweets'] = stringer.split(
            'statuses_count":')[1].split(',')[0]
    except:
        userdata['total_tweets'] = 'no data found'
    if args.verbose:
        t = BeautifulTable()
        # t.column_headers = ['Item', 'Value']
        t.append_row(["Full Name", OKBLUE+userdata['fullname']+ENDC])
        t.append_row(["Total Tweets", OKBLUE+userdata['total_tweets']+ENDC])
        t.append_row(["Followers count", OKBLUE+userdata['followers']+ENDC])
        t.append_row(["Following count", OKBLUE+userdata['following']+ENDC])
        t.append_row(["Listed count", OKBLUE+userdata['listed']+ENDC])
        t.append_row(["User Biography", OKBLUE+userdata['userbio']+ENDC])
        t.append_row(["User Location", OKBLUE+userdata['userlocation']+ENDC])
        t.append_row(["User Join Date", OKBLUE+userdata['userjoindate']+ENDC])
        t.append_row(["User Detailed Join Date", OKBLUE +
                      userdata['detailedcreated']+ENDC])
        t.append_row(["User Birth Date", OKBLUE +
                      userdata['userbirthdate']+ENDC])
        t.append_row(["User ID", OKBLUE+userdata['userid']+ENDC])
        print('\nBio table')
        print(t)
    return userdata


def get_tweets(username=args.username):
    url = f'https://twitter.com/i/profiles/show/{username}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{username}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.3 Safari/603.3.8',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    pages = 25
    alltweets = []
    while pages > 0:
        if pages == 25:
            jsondata = requests.get(url, headers=headers)
            actualjson = jsondata.json()
            souppage = BeautifulSoup(actualjson['items_html'], 'html.parser')
            tweets = souppage.find_all('li', class_='stream-item')
            try:
                last_tweet = tweets[19]["data-item-id"]
            except:
                pages = 1
        else:
            jsondata = requests.get(
                url, params={'max_position': last_tweet}, headers=headers)
            actualjson = jsondata.json()
            souppage = BeautifulSoup(actualjson['items_html'], 'html.parser')
            tweets = souppage.find_all('li', class_='stream-item')
        i = 0
        for item in tweets:
            tweetdict = dict()
            i = i + 1
            tweettext = item.find(class_='tweet-text')
            try:
                tweetdict['tweettext'] = tweettext.text
                tweetinfo = item.find('div', class_='tweet')
            except:
                tweetdict['tweettext'] = 'no tweet found'
                continue
            if tweetinfo.has_attr('data-retweeter'):
                tweetdict['type'] = 'retweet'
            else:
                tweetdict['type'] = 'original'
            retweets = item.find('span', class_='ProfileTweet-action--retweet')
            retweets = retweets.find('span')['data-tweet-stat-count']
            tweetdict['rts'] = retweets
            favorites = item.find(
                'span', class_='ProfileTweet-action--favorite')
            favorites = favorites.find('span')['data-tweet-stat-count']
            tweetdict['favs'] = favorites
            replies = item.find('span', class_='ProfileTweet-action--reply')
            replies = replies.find('span')['data-tweet-stat-count']
            tweetdict['replies'] = replies
            tweetdict['timestamp'] = item.find(
                class_='_timestamp')['data-time']
            # tweetid
            tweetdict['id'] = item["data-item-id"]
            # print(tweetdict)
            alltweets.append(tweetdict)
        if len(tweets) == 20 and pages > 0:
            last_tweet = tweets[19]["data-item-id"]
        pages = pages - 1
    if args.verbose:
        if len(alltweets) > 0:
            t = BeautifulTable()
            t.column_headers = [str(x) for x in alltweets[0].keys()]
            t.append_row([x for x in alltweets[0].values()])
            print('Most recent tweet')
            print(t)
    return alltweets


def get_stats(tweetslist):
    retweets, replies, favorites, rttype = [], [], [], []
    for item in tweetslist:
        if item['type'] == 'retweet':
            rttype.append(1)
            continue
        for k, v in item.items():
            if k == 'replies':
                replies.append(int(v))
            if k == 'rts':
                retweets.append(int(v))
            if k == 'favs':
                favorites.append(int(v))
    if args.verbose:
        if len(tweetslist) > 0:
            t = BeautifulTable()
            t.column_headers = ["Metric", "Amount"]
            t.append_row([f"Total tweets collected:",
                          f"{OKBLUE}{len(tweetslist)}{ENDC}"])
            t.append_row([f"Total that were retweets:",
                          f"{OKBLUE}{len(rttype)} ({round(len(rttype)/len(tweetslist)*100)}%) {ENDC}"])
            t.append_row([f"Retweets in {len(retweets)}",
                          f"{OKBLUE}{sum(retweets)}{ENDC}"])
            t.append_row([f"Replies in {len(replies)}",
                          f"{OKBLUE}{sum(replies)}{ENDC}"])
            t.append_row(
                [f"Favorites in {len(favorites)}", f"{OKBLUE}{sum(favorites)}{ENDC}"])
            print("\nMetrics table")
            print(t)

# main section


def main():
    """Main function that runs everything."""
    if args.nologo is not True:
        print(logo)
    if args.getff:
        followerslist = get_followers(args.username)
        print(followerslist)
        # followinglist = get_following(args.username)
    tweetslist = get_tweets(args.username)
    get_stats(tweetslist)
    userdatadict = get_user_data(args.username)
    if args.jsonout:
        with open('{}-tweets.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(tweetslist, indent=4,
                               sort_keys=True, default=str))
        with open('{}-profile.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(userdatadict, indent=4,
                               sort_keys=True, default=str))
        with open('{}-followers.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(followerslist, indent=4,
                               sort_keys=True, default=str))


if __name__ == "__main__":
    main()
