from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.amazon.pl/dp/B088MWX1FS")

get_price = driver.find_element(By.ID,"corePrice_feature_div").text.replace(' ','').split()
product_name = driver.title.split(':')[0]

print(product_name)
print(f'{get_price[0]},{get_price[1]}')

driver.close()