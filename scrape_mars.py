import time
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    # Create a dictionary for all of the scraped data
    mars_data = {} 
    # Visit the Mars news page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p
    
    # Weather
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    mars_data["featured_image_url"] = featured_image_url
        
    # Twitter
    twt_url = u'https://twitter.com/marswxreport?lang=en'
    re = requests.get(twt_url)
    twt_soup = BeautifulSoup(re.text, 'html.parser')

    mars_weather = [p.text.strip()
                for p in twt_soup.find_all('p', class_="tweet-text")]

    mars_weather = twt_soup[0]['text']
    
    mars_data["mars_weather"] = mars_weather
    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
   
    # Facts
    grab=pd.read_html(url3)
    mars_info=pd.DataFrame(grab[0])
    mars_info.columns=['Mars','Data']
    mars_table=mars_info.set_index("Mars")
    marsinformation = mars_table.to_html(classes='marsinformation')
    marsinformation =marsinformation.replace('\n', ' ')
    mars_data["mars_table"] = marsinformation
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemis=[]
    
    # Hemispheres
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = mars_hemis
    
    # Return the dictionary
    return mars_data
