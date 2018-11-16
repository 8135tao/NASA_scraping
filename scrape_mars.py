from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd


#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)

def init_browser(): 
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    def cook_soup(url):
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    mars_data={}


    nasa_news_soup = cook_soup('https://mars.nasa.gov/news/')
    list_of_news = nasa_news_soup.find_all('li',class_='slide')
    lastest_news_title = list_of_news[0].find('div',class_='content_title').text



    lastest_news_teaser = list_of_news[0].find('div',class_='article_teaser_body').text
    latest_news_date = list_of_news[0].find('div',class_='list_date').text


    mars_data['news title']=lastest_news_title
    mars_data['news teaser']=lastest_news_teaser
    mars_data['news date']=latest_news_date


    jpl_base_url = 'https://www.jpl.nasa.gov'
    url_pic = jpl_base_url+ '/spaceimages/?search=&category=Mars'
    jpl_pic_soup = cook_soup(url_pic)


    jpl_feature_img = jpl_pic_soup.find_all('a',class_= 'button fancybox')[0]
    jpl_feature_img_link = jpl_base_url+jpl_feature_img['data-link']


    jpl_large_pic_soup = cook_soup(jpl_feature_img_link)
    jpl_large_feature_img_link= jpl_base_url + jpl_large_pic_soup.find('article').find('figure',class_='lede').find('a')['href']

    mars_data['featured image link'] = jpl_large_feature_img_link

    twt_url='https://twitter.com/marswxreport?lang=en'
    twt_soup = cook_soup(twt_url)

    latest_weather_twt = twt_soup.find('div',class_='content').find('div',class_="js-tweet-text-container").find('p').text
    mars_data['mars weather'] = latest_weather_twt
    mars_data


    facts_url = 'https://space-facts.com/mars/'


    facts_tables = pd.read_html(facts_url)
    facts_df = facts_tables[0]
    facts_df.columns = ['properties', 'data']
    #facts_df.set_index('properties', inplace=True)

    facts_html_table = facts_df.to_html(index=False).replace('\n', '')
    mars_data['mars facts table'] = facts_html_table


    
    hemi_base_url = 'https://astrogeology.usgs.gov'
    hemi_url = hemi_base_url+'/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_soup = cook_soup(hemi_url)
    hemi_list = hemi_soup.find_all('div',class_='item')

    hemi_image_urls=[]
    for element in hemi_list:
        hemi_dict = {}
        link = hemi_base_url+element.find('a')['href']
        title = element.find('h3').text
        hemi_dict['title'] = title
        
        soup = cook_soup(link)
        ori_img_link = soup.find_all('a',target='_blank')[0]['href']
        hemi_dict['img_url'] = ori_img_link
        
        hemi_image_urls.append(hemi_dict)
        time.sleep(3)

    mars_data['hemisphere picture'] = hemi_image_urls
    

    return mars_data



