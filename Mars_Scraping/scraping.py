from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import lxml

#Initialize the browser, create a data dictionary and end webdriver to return scraped data
def scrape_all():
    #set the executable path and initialize a browser.
    executable_path = {'executable_path': 'C:/Users/Mobeen/.wdm/drivers/chromedriver/win32/91.0.4472.77/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere(browser)
    }
    
    browser.quit()
    return data

def mars_news(browser):
    
#Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
#Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_paragraph


# ### Featured Images 
def featured_image(browser):

# Visit Url 
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

# Find and click the full image button 
    full_image_elem = browser.find_by_tag('button')[1] # we want to click on the second button 
    full_image_elem.click()

#Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

# Find the relative image url 
    try: 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError: 
        return None
    
    # Use the base url to create an absolute url 
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url 


# # Scrape Mars Data: Mars Facts
def mars_facts():
    # Add try/except for error handling
        # Use 'read_html' to scrape the facts table into a dataframe
    df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]


    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere (browser):
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    hemisphere_image_urls = []
    for i in range(4): 
        x = 3 + i
        hemispheres = {}
        image_1 = browser.find_by_tag('img')[x]
        image_1.click()
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')
        title_1 = hemisphere_soup.find('div', class_='cover')
        title_1_text = title_1.find('h2', class_='title').text
        hemisphere_image_1 = []
        downloads_1 = hemisphere_soup.find('div', class_='downloads')
        image_1 = downloads_1.find('a').get('href')
        img_1_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_1}'
        hemispheres['img_url'] = img_1_url 
        hemispheres['title'] = title_1_text
        browser.back()
        hemisphere_image_urls.append(hemispheres)
    
    return hemisphere_image_urls

if __name__=="__main__":
    #If running as script, print scraped data
    print(scrape_all())




