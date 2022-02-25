from bs4 import BeautifulSoup
import requests

page_url = 'https://www.amazon.pl/Samsung-SM-G991BZADEUE-Model-Galaxy-Smartfon/dp/B08Q8L44GJ'
page = requests.get(page_url, cookies={'__hs_opt_out': 'no'})
soup = BeautifulSoup(page.content, 'html.parser')
product_name = soup.title.string.split(':')[0]
price = float(soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0','').replace(',','.'))

print(product_name)
print(price)
