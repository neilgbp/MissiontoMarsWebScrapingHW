import os
import pandas as pd
import pymongo
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver

print(os.path.abspath("chromedriver.exe"))

def init_browser():
    executable_path = {"executable_path": os.path.abspath("chromedriver.exe")} 
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_title = soup.find("div", class_="content_title").text
    mars_p = soup.find("div", class_="article_teaser_body").text

    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')

    img_html = browser.html
    soup = BeautifulSoup(img_html, "html.parser")
    img_path = soup.find('figure', class_='lede').a['href']
    feat_img_url = "https://www.jpl.nasa.gov" + img_path

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')
    table_data = soup.find('table', class_="tablepress tablepress-id-mars")
    table_all = table_data.find_all('tr')
    labels = []
    values = []

    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)

        mars_df = pd.DataFrame({
            "Label": labels,
            "Values": values
        })

    facts_table = mars_df.to_html(header=False, index=False)
    facts_table

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    usgs_html = browser.html
    soup = BeautifulSoup(usgs_html, "html.parser")
    mars_hemi = []

    results = soup.find("div", class_="collapsible results" )
    hemis = results.find_all("div", class_="item")

    for hemi in hemis:
        title = hemi.find("h3").text
        img_link = hemi.find("a")["href"]
        usgs_img_link = "https://astrogeology.usgs.gov" + img_link    
        browser.visit(usgs_img_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        usgs_img_url = downloads.find("a")["href"]
        mars_hemi.append({"title": title, "img_url": usgs_img_url})

    mars_dict = {
        "mars_title": mars_title,
        "mars_p": mars_p,
        "feat_img_url": feat_img_url,
        "mars_weather": mars_weather,
        "facts_table": facts_table,
        "hemi_images": mars_hemi
    }
    return mars_dict

if __name__  ==  "__main__":
    print(scrape())