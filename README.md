# PCOS
Data Scraping of PCOS Data using data from thelowdown

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Setup
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

urls = [
    "https://thelowdown.com/reviews/endo/465e36bf-4ffe-411c-a1a9-1757a42dbe65",
    "https://thelowdown.com/reviews/endo/0cefdd44-20be-4fe0-9fdf-30cae3479c61",
    "https://thelowdown.com/reviews/endo/fed1f9cc-72de-4d1d-bb99-32e09b635873",
    "https://thelowdown.com/reviews/endo/859fe79e-ed6d-45a2-b1d7-b45e45b0b95d",
    "https://thelowdown.com/reviews/endo/66957976-d9ed-4e0c-a9cc-2dc7e0a3419a",
    "https://thelowdown.com/reviews/endo/163ca055-c2a5-4ee5-8750-223472b30922",
    "https://thelowdown.com/reviews/endo/876e0001-d406-443f-a880-329db459eb18",
    "https://thelowdown.com/reviews/endo/703772ea-5cb9-4946-9c62-4d06a18b2e88",
    "https://thelowdown.com/reviews/endo/f641b273-b218-42eb-be69-65752e518119",
    "https://thelowdown.com/reviews/endo/5e22947c-7163-4537-bc35-1ec21d250d88",
    "https://thelowdown.com/reviews/endo/aae0fe2c-091a-46b7-be4d-e6bd26e4441f",
    "https://thelowdown.com/reviews/endo/215a480f-bfb5-492e-a0a3-4af3581a5f62",
    "https://thelowdown.com/reviews/endo/7003036b-8ece-4a72-b257-f805c4cd9cdf",
    "https://thelowdown.com/reviews/endo/931359d3-69c4-4334-bfea-e7f9b7b5db03",
    "https://thelowdown.com/reviews/endo/493546cb-bbab-4f7c-adc6-915519a5ad7d",
    "https://thelowdown.com/reviews/endo/9116b2c6-1513-4f7d-bc51-0e5f75de0168",
    "https://thelowdown.com/reviews/endo/fce5a27d-b15d-47a7-b5d4-d6983e752981",
    "https://thelowdown.com/reviews/endo/3f552e87-91d7-4639-bcbd-3ba705c9aa26",
    "https://thelowdown.com/reviews/endo/fed6ec83-f78c-46d5-bb28-9699bbfb1264",
    "https://thelowdown.com/reviews/endo/84587b33-f029-4f5f-8172-16a95dd10878",
    "https://thelowdown.com/reviews/endo/d9e08be1-5f00-48db-809f-2427424525fb",
    "https://thelowdown.com/reviews/endo/dedd021a-8999-4854-9bcd-417df12241a3",
    "https://thelowdown.com/reviews/endo/7ac2aab2-e4c0-4c9c-8b5b-da6fb13cca9e",
    "https://thelowdown.com/reviews/endo/194e0bd3-aa5b-4371-abbe-5cbceb10ade6",
    "https://thelowdown.com/reviews/endo/53f04c40-1cde-464a-996b-b95e5d94039d",
    "https://thelowdown.com/reviews/endo/6e16d943-2abf-422e-91df-f764b4f53753",
    "https://thelowdown.com/reviews/endo/6041e683-dacc-427e-9f00-db65fbd922b6",
    "https://thelowdown.com/reviews/endo/7feddfb9-c9c5-426b-a3fd-de914f7314d9",
    "https://thelowdown.com/reviews/endo/f2dcb5b3-b6a1-4327-b919-8e0fe589a27c",
    "https://thelowdown.com/reviews/endo/e80c019f-b698-4ff6-bce7-0af44f49a84d",
    "https://thelowdown.com/reviews/endo/eee59ac4-452e-4574-b914-b258e2e584a0",
    "https://thelowdown.com/reviews/endo/24885075-89a5-41cb-be49-b0664676807d",
    "https://thelowdown.com/reviews/endo/8c15f626-afa2-4915-9d88-f67bb9b2bb05",
    "https://thelowdown.com/reviews/endo/73536552-defc-4ec4-8351-51f010c2e139",
    "https://thelowdown.com/reviews/endo/ebc09a71-6fc9-4d8d-9395-83afc4fbf9d6",
    "https://thelowdown.com/reviews/endo/a95dc7b9-8daf-4e97-84e8-356071bedaf2",
    "https://thelowdown.com/reviews/endo/1f29c1cd-0623-4930-8904-b95105a3788e",
    "https://thelowdown.com/reviews/endo/edf85e2a-5b4f-4655-9d72-13c1f0e6292a",
    "https://thelowdown.com/reviews/endo/833ae581-6472-4f36-bf54-a84d5ad51d0c",
    "https://thelowdown.com/reviews/endo/fa7a76c6-a99e-41e3-90c3-0ab934d17431",
    "https://thelowdown.com/reviews/endo/622d9800-b1a6-4cc0-aead-f0bd4cf3cd04",
    "https://thelowdown.com/reviews/endo/ca2effbe-966b-4bc1-a9e9-4f85883987b0",
    "https://thelowdown.com/reviews/endo/c9edca2b-2c1a-45d2-83e8-20ef86d737f7",
    "https://thelowdown.com/reviews/endo/329ec105-ead8-4877-a602-c8f52985921c",
    "https://thelowdown.com/reviews/endo/259859e9-56a0-4a5d-a87d-60a2151972da",
    "https://thelowdown.com/reviews/endo/c81fd623-4bac-40d2-9f2f-adf53e1d6a48",
    "https://thelowdown.com/reviews/endo/27f3b276-04c0-42f2-9f8b-f8064e08a82e",
    "https://thelowdown.com/reviews/endo/6db67f04-dc44-4b65-add9-e362be0a85a4",
]

data = []  # List to hold the collected data

for url in urls:
    driver.get(url)

    try:
        # Wait for the review block to be visible
        review_block = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'MuiGrid-container') and contains(@class, 'css-13okyhu')]")
        ))

        # Extract the review text
        review_text = review_block.text
        print(f"Collected Review from {url}:")
        print(review_text)  # Debugging step to verify the text

        # Append the URL and review to the data list
        data.append((url, review_text))

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Close the driver
driver.quit()

# Check if data is populated before writing to CSV
if not data:
    print("No data to write to CSV.")
else:
    print("Writing data to CSV...")
    with open('scraped_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Review'])  # Write header row
        writer.writerows(data)  # Write the actual data rows

    print("Data has been saved to scraped_reviews.csv.")
