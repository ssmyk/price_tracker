import requests
from datetime import datetime
#requests.delete('http://10.1.1.11:5000/users/3')
#print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

'''
requests.post('http://localhost:5000/users/',json={
    "email": "w2w33323da@wsta33rt.pl",
    "password": "88888888888888888888888888888888888",
    "username": "1234"
  })
'''
'''
for i in range(6):
    requests.post('http://localhost:5000/products/',json={
        'product_name' : 'Motorola XYZ',
        'product_image' : 'https://m.media-amazon.com/images/I/61xHHgU0bYL._AC_SL1500_.jpg',
        'product_asin' : f'2FFVCC0JE3G',
        'date_added' : '20-12-12 13:24:22',
        'current_price' : '2394.43',
        'current_price_date' : '2021-12-12 13:24:22',
        'lowest_price' : '2100.12',
        'lowest_price_date' : '2021-12-12 13:24:22',
        'fk_user' : '1'
      })
'''
requests.post('http://localhost:5000/products/update',json={
        'product_asin' : 'B08QXG6Y6F',
        'date' : '2022-04-08 15:24:22',
        'price' : 23194.43,
        'fk_user' : '1'
      })

#requests.delete('http://localhost:5000/products/1')

