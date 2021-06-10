# Import Splinter, BeautifulSoup, and Pandas
import time
import pandas as pd 
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Convert html to soup object
    html = browser.html
    news_soup = bs(html, 'html.parser')

    
    slide_element = news_soup.select_one("ul.item_list li.slide")
    # Name first found a tag
    news_title = slide_elem.find("div", class_="content_title").get_text()
    # Find paragraph text
    news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    return news_title, news_p

def featured_image(browser):
    # Visit the URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find full image button and click
    full_image_element = browser.find_by_tag('button')[1]
    full_image_element.click()

    # Soupify from html
    html_page = browser.html
    html_soup = bs(html, 'html.parser')
    # Find the featured image
    try:
        featured_image = html_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{featured_imagel}'
    # Link to featured image
    return featured_image_url

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    hem_url=('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    browser.visit(hem_url)

    hemisphere_image_urls = []
    for i in range (4):
        time.sleep(10)
        images=browser.find_by_tag('h3')
        images[i].click()
        html=browser.html
        soup=bs(html,'html.parser')
        partial_url=soup.find('img',class_='wide-image')['src']
        image_title=soup.find('h2',class_='title').text
        image_url=f'https://astrogeology.usgs.gov{partial_url}'
        image_dict={'title':image_title,'image_url':image_url}
        hemisphere_image_urls.append(image_dict)
        browser.back()

    return hemisphere_image_urls
