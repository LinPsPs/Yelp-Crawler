# Yelp-Crawler
This is a crawler that can automatically download New York restaurant information on Yelp and save as a .csv file.
Currently, this crawler only works in New York area. But you could modify the url and BeautifulSoup codes inside the python script.  A possible way to modify it is to change the ```'New+York'``` keyword to other cities like ```'Detroit'```. But it might cause unexpected behaviors. The program might crash after modifications. Unless you have some basic ideas about website structures and BeautifulSoup, you should not edit the source code. Also, there is a hidden function ```restaurantMenuCrawler()```. This function is intended to download the menus from the restaurant pages, but some resturants just put links to their own website instead of using Yelp's menu website. This function will not work in most cases.

-----

### How to use
This program has a command line interface. You could use it with any shell.

1. You might install some packages used in this script. ```BeautifulSoup4, Pandas ...``` Check it in the import section.
2. Move to the folder containing this script. Sample: ```cd Project```
3. Call with python. ```Python Yelp-Crawler.py```

---

Important: The script contains some open source codes on the internet, since this code is open source as well. I will not include where these codes are from.

Enjoy.
