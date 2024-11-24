from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import time
import pandas as pd
import numpy as np

# Setup Selenium options
options = Options()

# Do NOT use headless mode initially to see the CAPTCHA/challenge
options.add_argument("--disable-gpu")

# Initialize the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


        
name_list = []
date_list = []
price_list = []
shop_code_list = []
JAN_code_list = []
brand_list = []
series_title_list = []
char_name_list = []
sculptor_list = []
size_list = []
gcode_list = []
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
        gcode = item['href']  # Extract the href attribute (the URL)
        gcode_list.append(gcode)
    pages += 1


base_link = "https://www.amiami.com"
count = 0

# Extracts HTML data of the individual figures
for gcode_url in gcode_list:
    figure_url = base_link + gcode_list[count]
    driver.get(figure_url)
    time.sleep(5)                       # Unsure if I need to add a sleep function here to prevent overloading the server. Referenced example has a waitTime variable of 5. 
    figure_html = driver.page_source

    try:
        figure_soup = BeautifulSoup(figure_html, "html.parser")
        item_details = figure_soup.findAll(class_ = ['item-detail__right', 'item-about'])
        item_about = figure_soup.findAll(class_ = ["item-about__data-text"], limit = 11)
        
        temp_list = []
        for i in item_about:
            temp_list.append(i.text)
            
        fig_name = figure_soup.find(class_ = ["item-detail__section-title"]).text
        fig_release_date = temp_list[0]
        fig_price = temp_list[1]
        fig_shop_code = temp_list[2]
        fig_JAN_code = temp_list[3]
        fig_brand = temp_list[4]
        fig_series_title = temp_list[5]
        fig_char_name = temp_list[6]
        if temp_list[7] == "The maximum purchase quantity for this item is 1 per account/shipping address.":
            fig_sculptor = np.nan
        else:
            fig_sculptor = temp_list[7]    
        
        item_specs = figure_soup.find(class_ = ["more"])
        
        specs = item_specs.get_text("|")    # Joins the bits of text together using | & clears out the <br/> tags
        splitSpecs = specs.split("|")       # Separates the long string into bits of strings so we can access stuff we want easier
        flag = 0
        for s in splitSpecs:
            if flag != 1:
                if "Size" in s:
                    fig_size = s
                    flag = 1               
        
        if flag == 0:
            for temp_item in temp_list:
                if flag == 0:
                    if "Size:" in temp_item or "Scale:" in temp_item:
                        fig_size = temp_item
                        flag = 1
            if flag == 0:
                fig_size = "Error"                
        
        name_list.append(fig_name)
        date_list.append(fig_release_date)
        price_list.append(fig_price)
        shop_code_list.append(fig_shop_code)
        JAN_code_list.append(fig_JAN_code)
        brand_list.append(fig_brand)
        series_title_list.append(fig_series_title)
        char_name_list.append(fig_char_name)
        sculptor_list.append(fig_sculptor)
        size_list.append(fig_size)
        count += 1

    except:
        print(figure_url)
        count += 1

driver.quit()

df_figure = pd.DataFrame(
    {'Name': name_list,
     'Release Date': date_list,
     'Price': price_list,
     'Shop Code': shop_code_list,
     'JAN Code': JAN_code_list,
     'Brand': brand_list,
     'Series Title': series_title_list,
     'Character Name': char_name_list,
     'Sculptor': sculptor_list,
     'Size Specifications': size_list
    })

fig_grade = ['A', 'A\-', 'B\+', 'B', 'C', 'J']      # "+" & "-" also included as regex expressions. "\" to match literal characters
box_grade = ['A', 'B', 'C', 'N']
bonus_grade = ['\[Bonus\]', '']
product_grade = [fr'\(Pre-owned ITEM:{fig}/BOX:{box}\){bonus}' for fig in fig_grade for box in box_grade for bonus in bonus_grade]

df_figure["Name"] = df_figure["Name"].replace(to_replace=product_grade, value='', regex=True)

with pd.ExcelWriter('Pre-Owned Prices.xlsx') as writer:
        df_figure.to_excel(writer, sheet_name='testing')
