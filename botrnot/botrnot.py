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
from bs4 import BeautifulSoup
import requests
from beautifultable import BeautifulTable

# globals
__version__ = "1.1.0"
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


def get_user_data(username):
    """Get user info for profile."""
    userdata = dict()
    r = requests.get(f'https://www.twitter.com/{username}')
    soup = BeautifulSoup(r.text, 'html.parser')
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
        userdata['fullname'] = twittername.text.strip()
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
    if args.verbose:
        t = BeautifulTable()
        # t.column_headers = ['Item', 'Value']
        t.append_row(["Full Name", OKBLUE+userdata['fullname']+ENDC])
        t.append_row(["Followers count", OKBLUE+userdata['followers']+ENDC])
        t.append_row(["Following count", OKBLUE+userdata['following']+ENDC])
        t.append_row(["User Biography", OKBLUE+userdata['userbio']+ENDC])
        t.append_row(["User Location", OKBLUE+userdata['userlocation']+ENDC])
        t.append_row(["User Join Date", OKBLUE+userdata['userjoindate']+ENDC])
        t.append_row(["User Birth Date", OKBLUE+userdata['userbirthdate']+ENDC])
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
            # print(tweets[19])
            last_tweet = tweets[19]["data-item-id"]
            # print(last_tweet)
        else:
            jsondata = requests.get(url, params={'max_position': last_tweet}, headers=headers)
            actualjson = jsondata.json()
            souppage = BeautifulSoup(actualjson['items_html'], 'html.parser')
            tweets = souppage.find_all('li', class_='stream-item')
        i = 0
        for item in tweets:
            tweetdict = dict()
            i = i + 1
            # print(item)
            tweettext = item.find(class_='tweet-text')
            tweetdict['tweettext'] = tweettext.text
            retweets = item.find('span', class_='ProfileTweet-action--retweet')
            retweets = retweets.find('span')['data-tweet-stat-count']
            # print(retweets)
            tweetdict['retweets'] = retweets
            favorites = item.find('span', class_='ProfileTweet-action--favorite')
            favorites = favorites.find('span')['data-tweet-stat-count']
            #print(favorites)
            tweetdict['favorites'] = favorites
            replies = item.find('span', class_='ProfileTweet-action--reply')
            replies = replies.find('span')['data-tweet-stat-count']
            tweetdict['replies'] = replies
            # timestamp
            tweetdict['timestamp'] = item.find(class_='_timestamp')['data-time']
            # tweetid
            tweetdict['id'] = item["data-item-id"]
            # print(tweetdict)
            alltweets.append(tweetdict)
        if len(tweets) == 20 and pages > 0:
            last_tweet = tweets[19]["data-item-id"]
        pages = pages - 1
    if args.verbose:
        t = BeautifulTable()
        t.column_headers = [str(x) for x in alltweets[0].keys()]
        t.append_row([x for x in alltweets[0].values()])
        print('Most recent tweet:\n')
        print(t)
    return alltweets


# main section


def main():
    """Main function that runs everything."""
    if args.nologo is not True:
        print(logo)

    tweetslist = get_tweets(args.username)
    if args.verbose:
        print(f"Total tweets collected: {len(tweetslist)}")
    # exit()
    userdatadict = get_user_data(args.username)
    # tweetslist = get_content(args.username)
    if args.jsonout:
        with open('{}-tweets.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(tweetslist, indent=4, sort_keys=True, default=str))
        with open('{}-profile.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(userdatadict, indent=4, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
