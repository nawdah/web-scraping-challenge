import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from splinter import Browser


def scrape():
    mars_dict = {}

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', executable_path, headless=True)

    # NASA Mars News
    url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search" \
           "=&category=19%2C165%2C184%2C204&blank_scope=Latest "

    browser.visit(url1)
    timeout = 5
    try:
        myElem = WebDriverWait(browser, timeout)
    except TimeoutException:
        print("Timed out waiting for page to load")
    time.sleep(5)

    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')

    news_title = soup1.find('div', class_="content_title").text
    news_p = soup1.find('div', class_="article_teaser_body").get_text()

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    # JPL Mars Space Images - Featured Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    timeout = 5
    try:
        myElem = WebDriverWait(browser, timeout)
    except TimeoutException:
        print("Timed out waiting for page to load")
    time.sleep(5)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    featured_image_url = soup2.find('a', class_="button fancybox")
    featured_image_url = featured_image_url.get('data-fancybox-href')
    featured_image_url = "https://www.jpl.nasa.gov" + str(featured_image_url)

    mars_dict['featured_image_url'] = featured_image_url

    # Mars Weather
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    timeout = 5
    try:
        myElem = WebDriverWait(browser, timeout)
    except TimeoutException:
        print("Timed out waiting for page to load")
    time.sleep(5)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    mars_weather = soup3.find('div',
                              class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim "
                                     "r-qvutc0").get_text()

    mars_dict['mars_weather'] = mars_weather

    # Mars Facts
    url4 = 'http://space-facts.com/mars/'
    tables = pd.read_html(url4)

    df = tables[2]
    df.columns = ['0', '1']
    mars_df = df.rename(columns={"0": "Description", "1": "Values"})
    mars_facts = mars_df.to_html()

    mars_dict['mars_facts'] = mars_facts

    # Mars Hemisphere
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    timeout = 5
    try:
        myElem = WebDriverWait(browser, timeout)
    except TimeoutException:
        print("Timed out waiting for page to load")
    time.sleep(5)

    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')

    hemisphere_image_urls = []

    images = soup5.find_all('div', class_='item')
    base_url = "https://astrogeology.usgs.gov"

    for image in images:
        title = image.find('h3').text
        image_url = image.find('a', class_="itemLink product-item")['href']
        browser.visit(base_url + image_url)
        img = browser.html
        soup = BeautifulSoup(img, 'html.parser')
        img_url = base_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict
