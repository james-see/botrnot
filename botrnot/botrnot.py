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
from bs4 import BeautifulSoup as bs
import requests
from beautifultable import BeautifulTable
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
    soup = bs(r.text, 'html.parser')
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
            souppage = bs(actualjson['items_html'], 'html.parser')
            tweets = souppage.find_all('li', class_='stream-item')
            try:
                last_tweet = tweets[19]["data-item-id"]
            except:
                pages = 1
        else:
            jsondata = requests.get(
                url, params={'max_position': last_tweet}, headers=headers)
            actualjson = jsondata.json()
            souppage = bs(actualjson['items_html'], 'html.parser')
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


# get following


def get_following(username):
    global followingdict
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{username}',
        'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    followerpage_base = requests.get(
        f'https://mobile.twitter.com/{username}/following?cursor=-1&count=200', headers=headers
        )
    # print(followerpage_base.text)
    soup = bs(followerpage_base.text, 'html.parser')
    users = soup.find_all('td', {'class': 'screenname'})
    for u in users:
        # print(u.text.strip())
        # print(u.find('a')['name'].strip())
        followingdict[u.find('a')['name'].strip()] = u.text.strip()
    if soup.find('div',{'class':'w-button-more'}):
        urlsnip = soup.find('div',{'class':'w-button-more'}).find('a')['href']
        return urlsnip
    else:
        return 0
        #users_data = get_more(urlsnip, users_data, username)


def get_more_following(urlsnip, username):
    global followingdict
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    updateddata = requests.get(f"https://mobile.twitter.com{urlsnip}&count=200", headers=headers)
    soup = bs(updateddata.text, 'html.parser')
    users = soup.find_all('td', {'class': 'screenname'})
    # print(len(users))
    if len(users) > 0:
        for u in users:
            followingdict[u.find('a')['name'].strip()] = u.text.strip()
    if soup.find('div',{'class':'w-button-more'}):
        urlsnip = soup.find('div',{'class':'w-button-more'}).find('a')['href']
        get_more_following(urlsnip, username)


# get followers


def get_followers(username):
    global followersdict
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{username}',
        'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    followerpage_base = requests.get(
        f'https://mobile.twitter.com/{username}/followers?cursor=-1&count=200', headers=headers
        )
    # print(followerpage_base.text)
    soup = bs(followerpage_base.text, 'html.parser')
    users = soup.find_all('td', {'class': 'screenname'})
    for u in users:
        # print(u.text.strip())
        # print(u.find('a')['name'].strip())
        followersdict[u.find('a')['name'].strip()] = u.text.strip()
    if soup.find('div',{'class':'w-button-more'}):
        urlsnip = soup.find('div',{'class':'w-button-more'}).find('a')['href']
        return urlsnip
    else:
        return 0
        #users_data = get_more(urlsnip, users_data, username)


def get_more_followers(urlsnip, username):
    global followersdict
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    updateddata = requests.get(f"https://mobile.twitter.com{urlsnip}&count=200", headers=headers)
    soup = bs(updateddata.text, 'html.parser')
    users = soup.find_all('td', {'class': 'screenname'})
    # print(len(users))
    if len(users) > 0:
        for u in users:
            followersdict[u.find('a')['name'].strip()] = u.text.strip()
    if soup.find('div',{'class':'w-button-more'}):
        urlsnip = soup.find('div',{'class':'w-button-more'}).find('a')['href']
        get_more_followers(urlsnip, username)


# main section

followingdict = dict()
followersdict = dict()

def main():
    """Main function that runs everything."""
    if args.nologo is not True:
        print(logo)
    if args.getff:
        global followingdict
        urlsnip = get_following(args.username)
        if urlsnip == 0:
            if args.verbose:
                t = BeautifulTable()
                t.column_headers = ["Username", "Full Name"]
                for k,v in followingdict.items():        
                    t.append_row([f"{k}",
                                f"{OKBLUE}{v}{ENDC}"])
                print("\nFollowing table")
                print(t)
        else:
            get_more_following(urlsnip,args.username)
            if args.verbose:
                t = BeautifulTable()
                t.column_headers = ["Username", "Full Name"]
                for k,v in followingdict.items():        
                    t.append_row([f"{k}",
                                f"{OKBLUE}{v}{ENDC}"])
                print("\nFollowing table")
                print(t)
        global followersdict
        urlsnip = get_followers(args.username)
        if urlsnip == 0:
            if args.verbose:
                t = BeautifulTable()
                t.column_headers = ["Username", "Full Name"]
                for k,v in followersdict.items():        
                    t.append_row([f"{k}",
                                f"{OKBLUE}{v}{ENDC}"])
                print("\nFollowing table")
                print(t)
        else:
            get_more_followers(urlsnip,args.username)
            if args.verbose:
                t = BeautifulTable()
                t.column_headers = ["Username", "Full Name"]
                for k,v in followersdict.items():        
                    t.append_row([f"{k}",
                                f"{OKBLUE}{v}{ENDC}"])
                print("\nFollowers table")
                print(t)


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
        with open('{}-following.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(followingdict, indent=4,
                               sort_keys=True, default=str))
        with open('{}-followers.json'.format(args.username), 'w+') as f:
            f.write(json.dumps(followersdict, indent=4,
                               sort_keys=True, default=str))

if __name__ == "__main__":
    main()
