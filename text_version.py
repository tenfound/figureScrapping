from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import time

# Setup Selenium options
options = Options()

# Do NOT use headless mode initially to see the CAPTCHA/challenge
# options.add_argument("--headless")  # You can enable this later
options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# class Figure:
#     def __init__(self, name, g_code, price, DOR, size):
#         self.name = name
#         self.g_code = g_code
#         self.price = price
#         self.DOR = DOR
#         self.size = size
        
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
    figure_url = base_link + gcode_list[0]
    print(figure_url)
    driver.get(figure_url)
    # time.sleep(10)                       # Unsure if I need to add a sleep function here to prevent overloading the server. Referenced example has a waitTime variable of 5. 
    figure_html = driver.page_source
    driver.quit()

    figure_soup = BeautifulSoup(figure_html, "html.parser")
    item_details = figure_soup.findAll(class_ = ['item-detail__right', 'item-about'])
    item_about = figure_soup.findAll(class_ = ["item-about__data-text"], limit = 8)
    
    fig_name = figure_soup.find(class_ = ["item-detail__section-title"])
    fig_release_date = item_about[0]
    fig_price = item_about[1]
    fig_shop_code = item_about[2]
    fig_JAN_code = item_about[3]
    fig_brand = item_about[4]
    fig_series_title = item_about[5]
    fig_char_name = item_about[6]
    fig_sculptor = item_about[7]
    
    item_specs = figure_soup.find(class_ = ["more"])
    # print(item_specs.prettify())
    
    specs = item_specs.get_text("|")    # Joins the bits of text together using | & clears out the <br/> tags
    splitSpecs = specs.split("|")       # Separates the long string into bits of strings so we can access stuff we want easier
    for s in splitSpecs:
        if "Size" not in s:
            continue
        else:
            fig_size = s
    
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

# figure = {'Name': fig_name,
#         'Release Date': fig_release_date,
#         'Price': fig_price,
#         'Shop Code': fig_shop_code,
#         'JAN Code': fig_JAN_code,
#         'Brand': fig_brand,
#         'Series Title': fig_series_title,
#         'Character Name': fig_char_name,
#         'Sculptor': fig_sculptor,
#        }
# df = pd.DataFrame(figure)
# df = df._append(df2, ignore_index = True)
