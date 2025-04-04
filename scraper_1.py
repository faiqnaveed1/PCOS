# Scrape all reviews to get individual links

import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

URL = "https://thelowdown.com/endometriosis/all-reviews"


# Set webdriver to use Chrome and go on Lowdown
driver = webdriver.Chrome()
driver.get(URL)
time.sleep(2)

try:
    # Keep going until there is no more "show more reviews" to press
    while True:
        # Find button
        elem = driver.find_element(By.ID, "showMoreReviews")
        time.sleep(1)
        # Scroll near it
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        time.sleep(1)
        # Scroll to exact location to ensure its clickable
        driver.execute_script("window.scrollBy(0, -400);")
        time.sleep(1)
        # Click
        elem.click()
except StaleElementReferenceException as ex:
    print()
except Exception as ex:
    print(type(ex))

# Once all reviews are loaded, find html source
html = driver.page_source
# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Save all reviews into a file
f = open("reviews.txt", "w")  # open file
for link in soup.find_all('a'): # find each element that may have a link
    curr_link = link.get('href')  # get the link we are currently looking at
    if curr_link is None:  # ensure the element we have actually does have a link
        continue
    elif "/reviews/endo/" in curr_link:  # ensure the link is one of the ones we want
        f.write(curr_link + "\n")  # add it to our file

f.close()  # close file
