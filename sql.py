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