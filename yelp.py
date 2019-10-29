from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from lxml.html import fromstring
import requests

import csv
import pandas as pd

import random
import re
import time
import sys
from itertools import cycle
import traceback

def printProgressBar (iteration, total, decimals = 1, length = 45, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % ("Progress:", bar, percent, "Complete"), end = '\r')
    if iteration == total: 
        print()

def restaurantInfoCrawler (searchRange: int, proxies: str, mode: bool):
    AttributeErrorNum = 0
    if mode:
        with open('yelp.csv', 'w', newline='') as of:
            f = csv.writer(of, delimiter=',')
            f.writerow(["restaurant_title", "restaurant_phoneNumber", "restaurant_address", "restaurant_numReview",
                        "restaurant_starCount", "restaurant_price", "restaurant_category", "restaurant_district", "restaurant_web"])
    proxies = { "http": "http://" + str(proxies), "https": "https://" + str(proxies)} 
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
    for i in range(0, searchRange, 30):
        headers = {"User-Agent": random.choice(user_agents)}
        page_html = None
        url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York&start=' + str(i)
        if mode:
            page_html = requests.get(url, headers=headers, proxies = proxies)
        else:
            page_html = requests.get(url, headers=headers)
        bs = soup(page_html.text, "html.parser")
        for item in bs.findAll('div', {'class': "lemon--div__373c0__1mboc largerScrollablePhotos__373c0__3FEIJ arrange__373c0__UHqhV border-color--default__373c0__2oFDT"}):
            try:
                restaurant_title = item.h3.get_text(strip=True)
                restaurant_web = item.find('a', {"class": 'lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5'}, href = True)
                restaurant_webAddress = "https://www.yelp.com" + restaurant_web['href']
                restaurant_title = re.sub(r'^[\d.\s]+', '', restaurant_title)
                restaurant_phoneNumber = item.select_one(
                    '[class*="secondaryAttributes"]').get_text(separator='|', strip=True).split('|')[0]
                restaurant_address = item.select_one(
                    '[class*="secondaryAttributes"]').get_text(separator='|', strip=True).split('|')[1]
                restaurant_numReview = item.select_one(
                    '[class*="reviewCount"]').get_text(strip=True)
                restaurant_numReview = re.sub(r'[^\d.]', '', restaurant_numReview)
                restaurant_starCount = item.select_one(
                    '[class*="stars"]')['aria-label']
                restaurant_starCount = re.sub(r'[^\d.]', '', restaurant_starCount)
                pr = item.select_one('[class*="priceRange"]')
                restaurant_price = pr.get_text(strip=True) if pr else '-'
                restaurant_category = [a.get_text(strip=True) for a in item.select(
                    '[class*="priceRange"] ~ span a')]
                restaurant_district = item.select_one(
                    '[class*="secondaryAttributes"]').get_text(separator='|', strip=True).split('|')[-1]
                # Enable if you want to see the entries in the terminal
                # print("Restaurant Name: " + restaurant_title)
                # print("Phone Number: " + restaurant_phoneNumber)
                # print("Address: " + restaurant_address)
                # print("Number of Reviews: " + restaurant_numReview)
                # print("Evaluation: " + restaurant_starCount)
                # print("Price: " + restaurant_price)
                # print("Category: " + ' '.join(restaurant_category))
                # print("District: " + restaurant_district)
                # print("Web: " + restaurant_webAddress)
                # print('-' * 60)
                # print('\n')
                if mode:
                    with open('yelp.csv', 'a+', newline='') as of:
                        f = csv.writer(of, delimiter=',')
                        f.writerow([restaurant_title, restaurant_phoneNumber, restaurant_address, restaurant_numReview,
                            restaurant_starCount, restaurant_price, restaurant_category, restaurant_district, restaurant_webAddress])
            except AttributeError:
                AttributeErrorNum += 1
                continue
        printProgressBar(i, searchRange)
        random_int = random.randint(1, 2)
        time.sleep(random_int)
    print('\nDone! Attribute Error Occurs ' + str(AttributeErrorNum) + ' Times')

def restaurantMenuCrawler(proxies: str, mode: bool):
    df = pd.read_csv('yelp.csv')
    webs = df["restaurant_web"]
    menuView = 'View Menu'
    proxies = { "http": "http://" + str(proxies), "https": "https://" + str(proxies)} 
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
    for web in webs:
        page_html = None
        headers = {"User-Agent": random.choice(user_agents)}
        url = web
        if mode:
            page_html = requests.get(url, headers=headers, proxies = proxies)
        else:
            page_html = requests.get(url, headers=headers)            
        bs = soup(page_html.text, "html.parser")
        menuPage = None
        try:
            infoBox = bs.find('div', {"class": 'lemon--div__373c0__1mboc island__373c0__3fs6U u-padding-t1 u-padding-r1 u-padding-b1 u-padding-l1 border--top__373c0__19Owr border--right__373c0__22AHO border--bottom__373c0__uPbXS border--left__373c0__1SjJs border-color--default__373c0__2oFDT background-color--white__373c0__GVEnp'})
            for info in infoBox.findAll("a", {"class": 'lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--default__373c0__1skgq'}):
                if str[info.find(text=True)] == menuView:
                    menuPage = info['href']
                else:
                    continue
        except AttributeError:
            print("Menu Page Not Find")
            continue
        url = menuPage
        if not mode:
            page_html = requests.get(url, headers=headers, proxies = proxies)  
        else:
            page_html = requests.get(url, headers=headers)
        bs = soup(page_html.text, "html.parser") 
        try:
            menu = bs.find('div', {"class": 'menu-sections'})
            for menuItem in menu.findAll('div', {"class": 'arrange_unit arrange_unit--fill'}):
                print(menuItem.find('div', {"class": 'arrange_unit arrange_unit--fill menu-item-details'}).find('h4').find('a').get_text(strip=True))
                print(menuItem.find('li', {"class": 'menu-item-price-amount'}).get_text(strip=True))
        except AttributeError:
            print("Menu Not Find")
            continue

if __name__ == '__main__':
    print('Yelp Crawler starts... (New York Version)')
    proxy = ' '
    invalidInput = True
    while invalidInput:
        isProxy = input('Use proxy(T/F): ')
        if isProxy.upper() == 'T' or isProxy.upper() == 'F':
            invalidInput = False
            if isProxy.upper == 'T':
                proxy = input('Please input the proxy: ')
        else:
            print('Invalid input. Please input T or F')
    invalidInput = True
    while invalidInput:
        searchRange = input('Please input search range(A num indicates how many yelp entries you want to get): ')
        if searchRange.isdigit():
            invalidInput = False
        else:
            print('You input is not a Num...\nTry again')
    if isProxy == 'T':
        restaurantInfoCrawler(int(searchRange), property, True)
    else:
        restaurantInfoCrawler(int(searchRange), property, False)