from itertools import product
from urllib import response
import requests
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

print(f"Setup for {os.getenv('ALIAS')}")
alias = os.getenv('ALIAS')

def get_headers():
    return {
        'User-Token':os.getenv('USER_TOKEN'),
        'User-Secret-Key':os.getenv('USER_SECRET_KEY')
    }


# You can see the related docs for this section at:
# https://docs.yampi.com.br/referencia-da-api/catalogo#produtos

def create_product(brand_id, name, description=""):
    data = {
    "simple": True,
    "brand_id": brand_id,
    # "erp_id": 1212,
    "active": True,
    "searchable": True,
    # "is_digital": False,
    # "buy_similars": False,
    # "priority": 1,
    # "rating": 5,
    # "ncm": "NCM",
    "name": name,
    # "slug": "produto-x",
    # "video": "https://youtube.com",
    "description": description,
    # "specifications": "Especificação",
    # "measures": "Medidas",
    # "gift_value": 1.00,
    # "seo_title": "Page title",
    # "seo_description": "Meta tag description",
    # "seo_keywords": "Meta tag keywords",
    # "canonical_url": "canonical_url",
    # "search_terms": "search, terms, for, better, search",
    # "categories_ids": [1, 2, 3, 4],
    # "flags_ids": [1, 2, 3, 4],
    # "filters_values_ids": [1, 2, 3, 4],
    # "variations_ids": [1, 2, 3, 4],
    # "similars_ids": [1, 2, 3, 4],
    # "skus": []
    }
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/products"
    response = requests.post(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"Product created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")


def create_sku(product_id,sku, price_cost, price_sale, image_url=None, weight=0.2,height=15,width=20, length=1):
    data = {
        "product_id": product_id,
        "sku": sku,
        # "erp_id": "01-753-Rose",
        # "barcode": "barcode-test",
        "price_cost": price_cost,
        "price_sale": price_sale,
        # "price_discount": 25,
        "weight": weight,
        "height": height,
        "width": width,
        "length": length,
        "quantity_managed": True,
        "availability": 0,
        "availability_soldout": -1,
        "blocked_sale": False,
        # "variations_values_ids": [490],
        # "customizations_ids": [1,2,3],
        "images": [
            {
                "url": image_url,
            }
        ]
    }
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/skus"
    response = requests.post(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"SKU created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")


def list_brands():
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/brands"
    response = requests.get(url=url, headers=get_headers())
    if (response.status_code == 200):
        return response.json()['data']
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")

def create_brand(name, featured= False):
    data = {
    "active": True,
    "featured": featured,
    "name": name,
    # "description": "Description test",
    # "logo_url": "http://foo.bar/logo.png",
    }
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/brands"
    response = requests.post(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"Brand created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")

def view_brands():
    list_b = list_brands()
    for b in list_b:
        print(f" ID: {b['id']}, NAME: {b['name']}")
    return list_b

def list_products():
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/products"
    response = requests.get(url=url, headers=get_headers())
    if (response.status_code == 200):
        return response.json()['data']
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")




data = pd.read_excel('saldo.xlsx')

brands = list_brands()
brand_names = [b['name'].lower() for b in brands]

products = list_products()
product_names = [b['name'].lower() for b in products]

print(data.keys())
brand_key = 'NOME SELO'

# for d in data[brand_key].unique():
#     if (d.lower() in brand_names):
#         print("Already existis")
#     else: 
#         print("Not exists, creating...")
#         create_brand(d)


brands = list_brands()
for i in range(len(data)):
    print(i)
    import pytest
    pytest.set_trace()
    name = d['TÍTULO']
    if (name.lower() in brand_names):
        print("Already existis")
    else:
        description = F"Autor: {data['AUTOR']}"
        brand_id = [b['id'] for b in brands if b['name'] == d[brand_key]]
        print("Not exists, creating...")
        print("Brand id")


