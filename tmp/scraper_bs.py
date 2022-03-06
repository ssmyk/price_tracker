from bs4 import BeautifulSoup
import requests

page_url = 'https://www.amazon.pl/Samsung-SM-G998BZSGEUE-Galaxy-Smartfon-Srebrny/dp/B08Q8MDFR1/'
page = requests.get(page_url, timeout=None)
soup = BeautifulSoup(page.content, 'html.parser')
product_name = soup.title.string.split(':')[0]
price = float(soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0','').replace(',','.'))
#image = soup.find('img')
#image = soup.find_all('data-old-hires')
#image = soup.find_all('img')
#image = soup.find(id = 'imgTagWrapperId')
#product_name = soup.find(id="landingImage")['alt']
image = soup.find(id="landingImage")['data-old-hires']


print(product_name)
print(price)
print(image)


#print(image.get('data-old-hires'))
