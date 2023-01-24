# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt
import re

# Set up Splinter
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
        
    }

    # Stop webdriver and return data
    browser.quit()

    return data

# Scrape Mars News
def mars_news(browser):

    # Visit the mars nasa news site
    # url = 'https://redplanetscience.com'
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `div` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):

    # Visit URL

    url = 'https://data-class-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    
    return img_url

# ## Mars Facts
def mars_facts():

    # The Pandas function read_html() specifically searches for and returns a list of 
    # tables found in the HTML.

    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe to HTML format, add bootstrap
    return df.to_html()

def mars_hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image = []

    html = browser.html
    title_soup = soup(html, 'html.parser')

    try:
        title_elems = title_soup.find_all('h3')

        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        for title_elem in title_elems:
            
            if title_elem.text == 'Back':
                break
            elif title_elem.text == '':
                continue

            image = title_elem.parent['href']
            imageTitle = title_elem.text
            image = f"{url}{image}"
            
            browser.visit(image)
            html = browser.html

            image_soup = soup(html, 'html.parser')
            image = image_soup.find('a', text='Sample').get('href')
            image = f"{url}{image}"

            hemisphere = {'image': image, 'title': imageTitle}
            hemisphere_image.append(hemisphere)

            browser.back()
        
    except AttributeError:
        return None
   
    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image

def mars_routes(browser):

    # Set default_url to a default image in case none are found.
    default_url = "https://mars.nasa.gov/system/resources/detail_files/26992_PIA24923_MAIN-web.jpg"

    # 1. Use browser to visit the URL 
    url = 'https://nasa.gov/'

    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    travel_soup = soup(html, 'html.parser')
    outer_container = ""

    try:    
        slide_elems = travel_soup.find_all('div.image')

        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        for slide_elem in slide_elems:
            
            image_href = slide_elem.find('a').get('href')

            if re.match('route', image_href, flags=re.IGNORECASE):
                outer_container = slide_elem
                break
            
        if outer_container == "":
            return default_url
        
        slide_elem = outer_container.find('div.list_image')

        image_src = slide_elem.find('img').get('src')
        image_url = f"{url}{image_src}"

    except AttributeError:
        return default_url
    
    # 4. Return the list that holds the dictionary of each image url and title.
    return image_url

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
