from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import time
import pandas as pd
import numpy as np

options = Options()

# Do NOT use headless mode initially to see the CAPTCHA/challenge
# options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
        
gcode_list = []
figures = []
pages = 1

while pages <= 2 :
    base_URL = "https://www.amiami.com/eng/search/list/?s_condition_flg=1&s_st_condition_flg=1&s_sortkey=preowned&pagecnt="
    final_URL = base_URL + str(pages)
    driver.get(final_URL)
    time.sleep(10)

    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    items = soup.find(class_='new-items__inner').findAll('a', href=True)

    # Extracts gcodes of figures on pre-owned page
    for item in items:
        gcode = item['href']
        gcode_list.append(gcode)
    pages += 1


base_link = "https://www.amiami.com"
count = 0

# Extracts HTML data of the individual figures
for gcode_url in gcode_list:
    figure_url = base_link + gcode_list[count]
    # print(figure_url)
    driver.get(figure_url)
    time.sleep(5)                       # Unsure if I need to add a sleep function here to prevent overloading the server. Referenced example has a waitTime variable of 5. 
    figure_html = driver.page_source
    try:
        figure_soup = BeautifulSoup(figure_html, "html.parser")        
   
        figure_info = {}

        for dl in figure_soup.findAll("dl"):
            for dt, dd in zip(dl.findAll("dt"), dl.findAll("dd")):
                key = dt.get_text(strip=True)
                if key == "Specifications":
                    value = dd.get_text("|")            # Joins the bits of text together using | & clears out the <br/> tags
                    value = value.split("|")            # Separates the long string into bits of strings so we can access stuff we want easier
                    for s in value:
                        if "Size" in s:
                            value = s
                else:
                    value = dd.get_text(strip=True)

                if "Notice" in key or "Customs" in key or "Copyright" in key or "Details" in key or "Product Line":
                    continue
                else:
                    figure_info[key] = value
        figures.append(figure_info)
        # print(figures)
        count += 1

    except:
        print(figure_url)
        count += 1
    # print(figure_url)

driver.quit()
figure_df = pd.DataFrame(figures)

with pd.ExcelWriter('Pre-Owned Prices.xlsx') as writer:
        figure_df.to_excel(writer, sheet_name='testing')
