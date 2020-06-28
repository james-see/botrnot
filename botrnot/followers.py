# "Get the followers"
import requests
from bs4 import BeautifulSoup as bs

def get_followers(username):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{username}',
        'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    followerpage_base = requests.get(
        f'https://mobile.twitter.com/{username}/followers', headers=headers
        )
    print(followerpage_base.text)
    soup = bs(followerpage_base.text, 'html.parser')
    users = soup.find_all('td', {'class': 'screenname'})
    users_data = dict()
    for u in users:
        print(u.text.strip())
        print(u.find('a')['name'].strip())
        users_data[u.find('a')['name'].strip()] = u.text.strip()
    return users_data