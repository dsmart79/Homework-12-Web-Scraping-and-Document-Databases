from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests

def init_browser(): 
    #executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', headless=False)

mars_info = {}

def scrape_mars_news():

    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title')
    news_p = soup.find('div', class_='article_teaser_body')

    mars_info['news_title'] = news_title.text
    mars_info['news_paragraph'] = news_p.text

    browser.quit()

    return mars_info

def scrape_mars_image():

    browser = init_browser()

    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)

    html_images = browser.html

    soup = BeautifulSoup(html_images, 'html.parser')

    featured_image_url = soup.find("img", class_="thumb")["src"]

    featured_image_full_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    featured_image_full_url

    mars_info['featured_image_full_url'] = featured_image_full_url

    browser.quit()

    return mars_info

def scrape_mars_weather():

    browser = init_browser()

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html_weather = browser.html

    soup = BeautifulSoup(html_weather, 'html.parser')

    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass

    mars_info['weather_tweet'] = weather_tweet
    
    browser.quit()

    return mars_info

def scrape_mars_facts():

    browser = init_browser()

    facts_url = 'http://space-facts.com/mars/'

    browser.visit(facts_url)

    mars_data = pd.read_html(facts_url)

    mars_data = pd.DataFrame(mars_data[0])

    mars_facts = mars_data.to_html(header = False, index = False)

    mars_info['mars_facts'] = mars_facts

    return mars_info

def scrape_mars_hemispheres():

    browser = init_browser()

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    html_hemispheres = browser.html

    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    for item in items: 
        title = item.find('h3').text
        
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemispheres_main_url + partial_img_url)
        
        
        partial_img_html = browser.html
        
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        img_url = hemispheres_main_url + soup.find('img', class_='thumb')['src']
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    mars_info['hemisphere'] = hemisphere_image_urls

    browser.quit()

    return mars_info
