import psycopg2
from bs4 import BeautifulSoup
import requests
from collections import deque

conn = psycopg2.connect(user="coderschool", database="tiki")
conn.autocommit= True 
cursor = conn.cursor()


def get_categories():
    cursor.execute("SELECT name FROM categories WHERE 1 <= id AND id <= 16")
    categories = cursor.fetchall()

    return categories


def check_category(name):
    cursor.execute("SELECT DISTINCT c.url, pcs.cate_lon FROM pcs JOIN categories as c ON pcs.cat_id = c.id;")
    check_list = cursor.fetchall()
    
    name_list = []
    for item in check_list:
        if name == item[0]:
            name_list.append(item[1])
    return name_list


def get_product(name):
    cursor.execute(f"SELECT p.name FROM pcs JOIN products as p ON pcs.cat_id = p.cat_id WHERE cate_lon LIKE '{name}';")
    product_list = cursor.fetchall()

    return product_list



