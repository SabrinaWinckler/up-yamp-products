from itertools import product
from urllib import response
import requests
import os
import pandas as pd
from unidecode import unidecode
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

def create_product(brand_id, name, description="", categories_ids=[], measures="",especification=""):
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
    "slug": unidecode(name.replace("-","x").replace("(","").replace(")","").replace(".","").replace("!","").replace("?","").replace("&","e").replace(":","x").replace(",","").replace(" ", "-").lower()),
    # "video": "https://youtube.com",
    "description": str(description),
    "specifications": especification,
    "measures": measures,
    # "gift_value": 1.00,
    "seo_title": name,
    # "seo_description": "Meta tag description",
    # "seo_keywords": "Meta tag keywords",
    # "canonical_url": "canonical_url",
    "search_terms": name.replace(" ", ",").lower(),
    "categories_ids": categories_ids, 
    # "flags_ids": [1, 2, 3, 4],
    # "filters_values_ids": [1, 2, 3, 4],
    # "variations_ids": [1, 2, 3, 4],
    # "similars_ids": [1, 2, 3, 4],
    # "skus": []
    }
    print(data)
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/products"
    response = requests.post(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"Product created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")

def update_product(product_id, description="", measures="",especification=""):
    data = {
        "description": str(description),
        "specifications": especification,
        "measures": measures
    }
    print(data)
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/products/{product_id}"
    response = requests.put(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"Product created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")


def create_sku(product_id,sku, price_cost, price_sale, image_url=None, weight=0.2,height=15,width=20, length=1):
    data = {
        "product_id": product_id,
        "sku": str(sku),
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
    print(data)
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/skus"
    response = requests.post(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"SKU created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")


def list_brands():
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/brands"
    list_of_brands = []
    response = requests.get(url=url, headers=get_headers())
    if (response.status_code == 200):
        data = response.json()['data']
        meta = response.json()['meta']['pagination']
        list_of_brands.append(data)
        for i in range(meta['total_pages']-1):
            url = meta['links']['next']
            response = requests.get(url=url, headers=get_headers())
            data = response.json()['data']
            meta = response.json()['meta']['pagination']
            list_of_brands.append(data)

        return list_of_brands
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
    print(data)
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/brands"
    response = requests.post(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"Brand created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")

def get_brands():
    list_b = list_brands()
    new_list = []
    for l in list_b:
        for b in l:
            new_list.append({'id': b['id'], 'name':b['name']})
    return new_list


def list_categories():
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/categories"
    list_of_categories = []
    response = requests.get(url=url, headers=get_headers())
    if (response.status_code == 200):
        data = response.json()['data']
        meta = response.json()['meta']['pagination']
        list_of_categories.append(data)
        for i in range(meta['total_pages']-1):
            url = meta['links']['next']
            response = requests.get(url=url, headers=get_headers())
            data = response.json()['data']
            meta = response.json()['meta']['pagination']
            list_of_categories.append(data)

        return list_of_categories
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")


def get_categories():
    list_b = list_categories()
    new_list = []
    for l in list_b:
        for b in l:
            new_list.append({'id': b['id'], 'name':b['name']})
    return new_list

def create_category(name, featured= False):
    data = {
    "active": True,
    "featured": False,
    "name": name,
    "slug": unidecode(name.replace("-","x").replace("(","").replace(")","").replace(".","").replace("!","").replace("?","").replace("&","e").replace(":","x").replace(",","").replace(" ", "-").lower()),
    "seo_title": name,
    "seo_keywords": name.replace(" ", ",").lower(),
    # "seo_description": "Seo description",
    # "banners_ids": [1, 2, 3],
    # "external_url": "http://www.link.com",
    # "canonical_url": "http://www.link.com"
    }
    print(data)
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/categories"
    response = requests.post(url=url,headers=get_headers(),json=data)
    if (response.status_code == 200):
        print(f"Category created {response.json()}")
        return response.json()
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")
        if ("slug" in response.json()['errors'].keys()):
            data['slug']=None
            response = requests.post(url=url,headers=get_headers(),json=data)
            if (response.status_code == 200):
                print(f"Category created {response.json()}")
                return response.json()
            else:
                print(f"Error getting response from: {url} /n Error: {response.json()}")                

def list_products():
    url = f"https://api.dooki.com.br/v2/{alias}/catalog/products"
    list_of_products = []
    response = requests.get(url=url, headers=get_headers())
    if (response.status_code == 200):
        data = response.json()['data']
        meta = response.json()['meta']['pagination']
        list_of_products.append(data)
        for i in range(meta['total_pages']-1):
            url = meta['links']['next']
            response = requests.get(url=url, headers=get_headers())
            data = response.json()['data']
            meta = response.json()['meta']['pagination']
            list_of_products.append(data)

        return list_of_products
    else:
        print(f"Error getting response from: {url} /n Error: {response.json()}")


def get_products():
    list_b = list_products()
    new_list = []
    for l in list_b:
        for b in l:
            new_list.append({'id': b['id'], 'name':b['name']})
    return new_list


data = pd.read_excel('saldo_tudo.xlsx')
infos_csv = pd.read_csv('infos1.csv')

brands = get_brands()
brand_names = [b['name'].lower() for b in brands]

categories = get_categories()
categories_names = [c['name'].lower() for c in categories]

products = get_products()
product_names = [b['name'].lower() for b in products]

print(data.keys())
brand_key = 'NOME SELO'
name_key = 'TÍTULO'
category_key = 'GRUPO'

for d in data[brand_key].unique():
    if (d.lower() in brand_names):
        print("Already existis")
    else: 
        print("Not exists, creating...")
        create_brand(d)

for d in data[category_key].unique():
    if (d.lower() in categories_names):
        print("Already existis")
    else: 
        print("Not exists, creating...")
        create_category(d)

brands = get_brands()
categories = get_categories()
errors = []

print(f"{len(data)} Products")
for i in range(len(data)):
    name = data.loc[i][name_key]
    print(f"Position {i} Name {name}")
    if (str(name).lower() in product_names):
        print("Already existis")
    else:
        isbn = data.loc[i]['ISBN']
        # GET INFOS AND VERIFY DATA
        infos = infos_csv.loc[(infos_csv['ISBN'])==isbn]
        if (infos.empty):
            print(f"Not existis yet... {isbn}")
            errors.append(f"Not existis yet... {isbn}")
            df = pd.DataFrame(errors)
            df.to_csv("errors.csv")
            continue
        elif ('Not Found' in infos['image'].values[0]):
            print(f"Not Founded yet... {isbn}")
            errors.append(f"Not Founded yet... {isbn}")
            df = pd.DataFrame(errors)
            df.to_csv("errors.csv")
            continue

        print("Regitering...")
        description = F" {infos['description'].values[0]} \n Autor: {data.loc[i]['AUTOR']}"
        brand_id = [b['id'] for b in brands if str(b['name']).lower() == data.loc[i][brand_key].lower()][0]
        list_category_ids = [c['id'] for c in categories if str(c['name']).lower() == data.loc[i][category_key].lower()]
        image = infos['image'].values[0]
        weight = infos['weight'].values[0].split('g')[0]
        print( infos['weight'].values[0])
        if ('K' in weight):
            weight = float(weight.split('K')[0])*100
        else:
            weight = float(weight)

        dimensions = infos['dimensions'].values[0].split("x")
        try:
            height=float(dimensions[-1].split('c')[0].replace(",",".")) 
            width=float(dimensions[-2].split('c')[0].replace(",","."))
            length=float(dimensions[0].split('c')[0].replace(",",".")) 
        except:
            especification = infos['especification'].values[0]
            weight_info = [especification[i+1] for i in range(len(especification)) if especification[i] == "Peso:"]
            weight = weight_info.split('g')[0]
            if ('K' in weight):
                weight = float(weight.split('K')[0])*100
            else:
                weight = float(weight)

            dimensions = [especification[i+1] for i in range(len(especification)) if especification[i] == "Dimensões:"]
            height=float(dimensions[-1].split('c')[0].replace(",",".")) 
            width=float(dimensions[-2].split('c')[0].replace(",","."))
            length=float(dimensions[0].split('c')[0].replace(",",".")) 
            

        price_sale=float(data.loc[i]['PREÇO CAPA'].replace(",","."))
        price_cost=price_sale-(price_sale*(10/100))
        # CREATE PRODUCT
        product_response = create_product(brand_id=brand_id,name=name,description=description,categories_ids=list_category_ids,measures=infos['dimensions'].values[0],especification=str(infos['especification'].values[0]).split("cm")[-1].replace("[","").replace("]","").replace(",","\n").replace("'FICHA TÉCNICA'","").replace("'",""))
        product_id = product_response['data']['id']
        # CREATE SKU
        create_sku(product_id=product_id,sku=isbn,price_cost=price_cost, price_sale=price_sale, image_url=image, weight=weight, width=width, length=length, height=height)





