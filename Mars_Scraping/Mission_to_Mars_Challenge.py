#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


#set the executable path and initialize a browser.
executable_path = {'executable_path': 'C:/Users/Mobeen/.wdm/drivers/chromedriver/win32/89.0.4389.23/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)
#Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
#With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.
#One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). 
#As an example, ul.item_list would be found in HTML as <ul class="item_list">.
#Secondly, we're also telling our browser to wait one second before searching for components. 
#The optional delay is useful because sometimes dynamic pages take a little while to load, 
#especially if they are image-heavy.


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p
#There are two methods used to find tags and attributes with BeautifulSoup:
#.find() is used when we want only the first class and attribute we've specified.
#.find_all() is used when we want to retrieve all of the tags and attributes.
#For example, if we were to use .find_all() instead of .find() when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one.


# In[8]:


#Scrape Mars Data: Featured Image
#Ultimately, with each item we scrape, we'll also save and then serve it on our own website. 
#We're basically using pieces from other websites to piece together our own website, 
#with news and images custom tailored to Robin's taste.


# ### Featured Images 

# In[9]:


# Visit Url 
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[10]:


# Find and click the full image button 
full_image_elem = browser.find_by_tag('button')[1] # we want to click on the second button 
full_image_elem.click()


# In[11]:


#Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url 
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
#We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
#Let's break it down:
#An img tag is nested within this HTML, so we've included it.
#.get('src') pulls the link to the image.
#What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. 
#Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."


# In[13]:


#We pulled the link of the image 
#this is the partial link, base url isn't included 
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url
#We're using an f-string for this print statement because it's a cleaner way to create print statements; 
#they're also evaluated at run-time. This means that it, and the variable it holds, 
#doesn't exist until the code is executed and the values are not constant. This works well for our scraping app because the data we're scraping is live and will be updated frequently.


# # Scrape Mars Data: Mars Facts

# In[14]:


# In this case all the facts we want are conveniently stored into a table 
# Instead of scraping each row we will scrape the entire table with pandas read._html() function
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
#y specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
#Then, it turns the table into a DataFrame.
df.columns=['description', 'Mars', 'Earth']
#Here, we assign columns to the new DataFrame for additional clarity.
df.set_index('description', inplace=True)
#we're turning the Description column into the DataFrame's index. 
#inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df


# In[15]:


#This is exactly what Robin is looking to add to her web application. 
#How do we add the DataFrame to a web application? 
#Thankfully, Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function. 
#Add this line to the next cell in your notebook and then run the code.
df.to_html


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# # Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)


# In[17]:


image_1 = browser.find_by_tag('img')[3]
image_1.click()


# In[18]:


html = browser.html
hemisphere_soup = soup(html, 'html.parser')


# In[19]:


title_1 = hemisphere_soup.find('div', class_='cover')
title_1_text = title_1.find('h2', class_='title').text
title_1_text 


# In[20]:


downloads_1 = hemisphere_soup.find('div', class_='downloads')
image_1 = downloads_1.find('a').get('href')
image_1


# In[21]:


img_1_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_1}'
img_1_url


# In[22]:


browser.back()


# In[23]:


image_2 = browser.find_by_tag('img')[4]
image_2.click()


# In[24]:


html = browser.html
hemisphere_soup = soup(html, 'html.parser')


# In[25]:


title_2 = hemisphere_soup.find('div', class_='cover')
title_2_text = title_2.find('h2', class_='title').text
title_2_text 


# In[26]:


downloads_2 = hemisphere_soup.find('div', class_='downloads')
image_2 = downloads_2.find('a').get('href')
image_2


# In[27]:


img_2_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_2}'
img_2_url


# In[28]:


browser.back()


# In[29]:


image_3 = browser.find_by_tag('img')[5]
image_3.click()


# In[30]:


html = browser.html
hemisphere_soup = soup(html, 'html.parser')


# In[31]:


title_3 = hemisphere_soup.find('div', class_='cover')
title_3_text = title_3.find('h2', class_='title').text
title_3_text 


# In[32]:


downloads_3 = hemisphere_soup.find('div', class_='downloads')
image_3 = downloads_3.find('a').get('href')
image_3


# In[39]:


img_3_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_3}'
img_3_url


# In[34]:


browser.back()


# In[35]:


image_4 = browser.find_by_tag('img')[6]
image_4.click()


# In[36]:


html = browser.html
hemisphere_soup = soup(html, 'html.parser')


# In[37]:


title_4 = hemisphere_soup.find('div', class_='cover')
title_4_text = title_4.find('h2', class_='title').text
title_4_text


# In[38]:


downloads_4 = hemisphere_soup.find('div', class_='downloads')
image_4 = downloads_4.find('a').get('href')
image_4


# In[40]:


img_4_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_4}'
img_4_url


# In[ ]:


browser.back()


# In[64]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)


# In[78]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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
#     image_2 = browser.find_by_tag('img')[4]
#     html = browser.html
#     hemisphere_soup = soup(html, 'html.parser')
#     title_2 = hemisphere_soup.find('div', class_='cover')
#     title_2_text = title_2.find('h2', class_='title').text
#     downloads_2 = hemisphere_soup.find('div', class_='downloads')
#     image_2 = downloads_2.find('a').get('href')
#     img_2_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_2}'
#     hemispheres['img_url'] = img_2_url 
#     hemisphere['title'] = title_2_text
#     browser.back()
#     image_3 = browser.find_by_tag('img')[5]
#     image_3.click()
#     html = browser.html
#     hemisphere_soup = soup(html, 'html.parser')
#     title_3 = hemisphere_soup.find('div', class_='cover')
#     title_3_text = title_3.find('h2', class_='title').text
#     downloads_3 = hemisphere_soup.find('div', class_='downloads')
#     image_3 = downloads_3.find('a').get('href')
#     img_3_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_3}'

#     hemispheres['img_url'] = img_3_url 
#     hemisphere['title'] = title_3_text
#     browser.back()
#     image_4 = browser.find_by_tag('img')[6]
#     image_4.click()
#     html = browser.html
#     hemisphere_soup = soup(html, 'html.parser')
#     title_4 = hemisphere_soup.find('div', class_='cover')
#     title_4_text = title_4.find('h2', class_='title').text
#     downloads_4 = hemisphere_soup.find('div', class_='downloads')
#     image_4 = downloads_4.find('a').get('href')
#     img_4_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{image_4}'
#     browser.back()
#     hemispheres['img_url'] = img_4_url 
#     hemisphere['title'] = title_4_text
#     hemisphere_image_url.append(hemisphere)
    


# In[77]:


hemisphere_image_urls


# In[ ]:


browser.quit()
#To fully automate jupyter notebook need to convert into .py file 

