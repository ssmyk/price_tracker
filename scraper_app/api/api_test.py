import requests

requests.post('http://localhost:5000/products/',json={
        'product_name' : 'Motorola XYZ',
        'product_asin' : f'2FVSR0JE3G',
        'date_added' : '2021-12-12 13:24:22',
        'current_price' : '2394.43',
        'current_price_date' : '2021-12-12 13:24:22',
        'lowest_price' : '2100.12',
        'lowest_price_date' : '2021-12-12 13:24:22',
        'fk_user' : '1'})