from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://www.olx.in/items/q-car-cover"
driver.get(url)


try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-aut-id='itemTitle']"))
    )
except:
    print("Timeout: Listings not found.")
    driver.quit()
    exit()


time.sleep(2) 
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

results = []

for a_tag in soup.find_all("a", href=True):
    if "item" in a_tag["href"]:
        title = a_tag.find('span', {'data-aut-id': 'itemTitle'})
        price = a_tag.find('span', {'data-aut-id': 'itemPrice'})
        location = a_tag.find('span', {'data-aut-id': 'item-location'})

        if title and price and location:
            results.append({
                "Title": title.text.strip(),
                "Price": price.text.strip(),
                "Location": location.text.strip(),
                "Link": "https://www.olx.in" + a_tag["href"]
            })

df = pd.DataFrame(results)
df.to_csv('olx_car_covers.csv', index=False)
print(f" Scraped {len(df)} listings. Data saved to olx_car_covers.csv")
