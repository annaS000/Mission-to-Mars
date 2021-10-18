# Import Splinter and BeautifulSoup
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='thumbimg').get('src')

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ## Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# Parse the resulting html with soup
html = browser.html
imgs = soup(html, 'html.parser')
titles = [str(i.text) for i in imgs.find_all('h3')[:-1]]

# 2. Create a list to hold the images and titles.
# 3. Write code to retrieve the image urls and titles for each hemisphere.
urls = []
for i in titles:
    browser.find_by_text(i).click()
    full = url+soup(browser.html,'html.parser').find('a',text='Sample').get('href')
    urls.append(full)
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls = [{'img_url':i,'title':j} for i,j in zip(urls,titles)]

# 5. Quit the browser
browser.quit()

