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



def get_sub_category(category_name):
    cursor.execute(f"SELECT b.name FROM categories a LEFT JOIN categories b ON a.id = b.parent_id WHERE a.name LIKE '{category_name}';")
    sub_categories = cursor.fetchall()

    return sub_categories


def get_all_sub(category_id):
    cursor.execute(f"SELECT id FROM categories WHERE parent_id = {category_id};")
    subs = tuple(x[0] for x in cursor.fetchall())
    result = []
    while subs:
#         result.extend(subs)
        result = subs
        cursor.execute(f"SELECT id FROM categories WHERE parent_id IN {subs}")
        subs = tuple(x[0] for x in cursor.fetchall())
    return result


def get_product(category_name,page, command = None):
    cursor.execute(f"SELECT id FROM categories WHERE name LIKE '{category_name}';")
    id_ = cursor.fetchall()[0][0]
    if len(get_all_sub(id_)) != 0:
        cursor.execute(f"SELECT name, img FROM products WHERE cat_id IN {get_all_sub(id_)} LIMIT 12 OFFSET {page*12};")
        products = cursor.fetchall()
    else:
        cursor.execute(f"SELECT name, img FROM products WHERE cat_id = {id_} LIMIT 12 OFFSET {page*12};")
        products = cursor.fetchall()

    pages = (len(products) // 12)

    return products, pages



def get_same_level_sub(category_name):
    cursor.execute("SELECT b.name \
                    FROM (SELECT * FROM categories WHERE name = 'Tivi') a \
                    RIGHT JOIN categories b \
                    ON a.parent_id = b.parent_id \
                    WHERE a.name IS NOT NULL;"
                    )
    result = cursor.fetchall()
    return result 
