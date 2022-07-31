# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

# create scrape function
def scrape():
    browser = init_browser()

     # use browser to open the url 
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")

    # get the latest news
    data = news_soup.select_one('ul.item_list li.slide')
    news_title = data.find("div", class_='content_title').text.strip()
    news_p = data.find('div', class_="article_teaser_body").text.strip()


     # for Mars latest image visit the url and get the full image url
    img_url = 'https://spaceimages-mars.com/'

    # use browser to open the url for image
    browser.visit(img_url) 

    # create html to parse
    html = browser.html

    # create soup object to parse html
    soup = bs(html, "html.parser")

    # use beautifulsoup to navigate to the image
    image = soup.find_all('img')[1]["src"]

    # create the url for the image
    featured_image_url = 'https://spaceimages-mars.com/' + image

     # Mars facts
    # get the url for Mars's facts 
    Facts_URL = "https://galaxyfacts-mars.com/"

    # Use panda's `read_html` to parse the url
    Facts_Table = pd.read_html(Facts_URL)

    # convert table to pandas dataframe
    Facts_df = Facts_Table[1]

    #rename the columns
    Facts_df.columns=["Description", "Value"]

    # reset the index for the df
    Facts_df.set_index("Description", inplace=True)
    # convert dataframe to an html table string
    Facts_HTML = Facts_df.to_html()

    # Mars hemisphere
    # get the url and open it with browser
    h_url = "https://marshemispheres.com/"
    browser.visit(h_url)
    # cerate html 
    html = browser.html

    # use beautiful soup to create soup object
    soup = bs(html, "html.parser")

    data = soup.find_all("div", class_="item")
    
    # cretae a list to hold data for hemispheres
    hemisphere_img_urls = []

    # loop the data list to find titles and img urls for hemispheres
    for d in data:
    
        title = d.find("h3").text
    
        img_url = d.a["href"]
    
        url = "https://marshemispheres.com/" + img_url
    
        # use requests to get full images url 
        response = requests.get(url)
    
        # create soup object
        soup = bs(response.text,"html.parser")
    
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
    
        # create full image url
        full_url = "https://marshemispheres.com/" + new_url
    
   
        #make a dict and append to the list
        hemisphere_img_urls.append({"title": title, "img_url": full_url})

    # create mars data dictionary to hold data
    Mars_data = {
        "news_title": news_title,
        "paragraph" : news_p,
        "featured_image_url": featured_image_url,
        "html_table": Facts_HTML,
        "hemisphere_img_urls": hemisphere_img_urls
    }

     # close the browser after scraping
    browser.quit()

    # return results
    return Mars_data