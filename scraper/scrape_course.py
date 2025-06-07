from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")  # run in background

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://tds.s-anand.net/#/2025-01/")
time.sleep(5)  # wait for JS to load

# Expand all content blocks by clicking headings
elements = driver.find_elements("css selector", ".accordion-title")
for el in elements:
    driver.execute_script("arguments[0].click();", el)
    time.sleep(0.5)

# Now extract all visible text
page_content = driver.find_element("tag name", "body").text

# Save to file
with open("scraper/tds_course_content.txt", "w", encoding="utf-8") as f:
    f.write(page_content)

driver.quit()
print("✅ TDS Course Content scraped and saved.")
