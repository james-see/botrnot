from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from getpass import getpass
from bs4 import BeautifulSoup

def login_twitter(username, password, cwebdriver):
    driver = cwebdriver
    driver.get("https://twitter.com/login")

    username_field = driver.find_element_by_name("session[username_or_email]")
    password_field = driver.find_element_by_name("session[password]")

    username_field.send_keys(username)
    driver.implicitly_wait(1)
    
    password_field.send_keys(password)
    driver.implicitly_wait(1)

    driver.find_element_by_class_name("r-urgr8i").click()
    return driver


def load_profile(profilename, cdriver):
    partialurl_following = f'https://twitter.com/{profilename}/following'
    partialurl_followers = f'https://twitter.com/{profilename}/followers'
    following = cdriver.get(partialurl_followers)
    figureitout = cdriver.find_element_by_class_name("css-1dbjc4n")
    print(figureitout)
    tutorial_soup = BeautifulSoup(figureitout.get_attribute('innerHTML'), 'html.parser')
    justdivs = tutorial_soup.find_all('div', {'class','css-1dbjc4n'})
    for item in justdivs:
        print(item)


if __name__ == "__main__":
    chrome_driver_path = './runners/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    cwebdriver = webdriver.Chrome(
        executable_path=chrome_driver_path, options=chrome_options
    )
    username = input("user name : ")
    password = getpass("password  : ")
    logindata = login_twitter(username, password, cwebdriver)
    profilename = input("username to lookup followers and friends : ")
    profiledata = load_profile(profilename, logindata)
    print(profiledata)
    cwebdriver.close()
    logindata.close()