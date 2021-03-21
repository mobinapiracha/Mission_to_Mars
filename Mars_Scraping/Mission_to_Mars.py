# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#set the executable path and initialize a browser.
executable_path = {'executable_path': 'C:/Users/Mobeen/.wdm/drivers/chromedriver/win32/89.0.4389.23/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

#Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)
#Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

#Scrape Mars Data: Featured Image

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
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#We pulled the link of the image 
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

# # Scrape Mars Data: Mars Facts
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html

browser.quit()


