import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

CHROME_DRIVER_PATH = "D:\Development\chromedriver.exe"
REAL_ESTATE_URL = "https://www.domain.com.au/rent/fletcher-nsw-2287/?excludedeposittaken=1"
GOOGLE_FORM_URL = MY_GOOGLE_FORM


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(REAL_ESTATE_URL, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

property_prices = soup.find_all("p", class_="css-mgq8yx")
price_list = [item.text.split()[0].replace("$", "") for item in property_prices]
# print(f"{price_list}\n{len(price_list)}")

property_addresses = soup.find_all("h2", class_="css-bqbbuf")
address_list = [item.text.replace('\xa0', ' ') for item in property_addresses]
# print(f"{address_list}\n{len(address_list)}")

property_links = soup.find_all("a", class_="address is-two-lines css-1y2bib4")
link_list = [item["href"] for item in property_links]
# print(f"{link_list}\n{len(link_list)}")

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

for index in range(len(price_list)):
    driver.get(GOOGLE_FORM_URL)

    time.sleep(1)

    answer_address = driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    answer_price = driver.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    answer_link = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')



    answer_address.send_keys(address_list[index])
    answer_price.send_keys(price_list[index])
    answer_link.send_keys(link_list[index])

    # time.sleep(1)

    submit_button.click()

    # time.sleep(1)


driver.quit()

