# 1. Project Name
- Web Crawler

# 2. Description

**Tiki Web Scraping** is a project to collect, organize, and store data about the available products on tiki.vn using Data Learning.

The scope of the project covers 100.000 products in all the main categories and its first sub-categories. 


# 3. Installation
- You need to install Python, Flask, Postgresql, psycopg2, BeautifulSoup, Anaconda


# 4. Guide
1. Log in your Postgresql user (say "your_username") and create a new database (say "your_db_name")


2. Crawl 10 pages from each category in Tiki and store the data in Postgresql database
- Run scrape_store.py file in Terminal: `python scrape_store.py`
- Input your Postgresql user name, new database name and your password
- Wait until done 

3. Now you have 2 tables : 'categories' and 'products'
* Categories tables.

| Field Name | Type | 
| --------   | -------- |
| ID | INTEGER | 
| Name       | VARCHAR (255)|
| Parent ID | INTEGER |

* Product Table

| Field Name | Type | 
| --------   | -------- | 
| ID | INTEGER |
| Data ID | INTEGER 
| Seller ID | INTEGER
| Name      | VARCHAR (255)|
| Price | INTEGER|
| Image Link | TEXT
| Category ID | INTEGER |

![](https://i.imgur.com/U2ojQq0.jpg)

4. Run `app.py` , open your browser, type your localhost address and explore
* app.py will :

 Connect database to FlaskApp.  
 Visualize database using html, CSS.  


Some added features: 
1. Main categories link to sub categories. 
2. Price Filter: High to Low, Low to High. 
3. Paginations. 
4. Search tool. 

You can see more details in python script files, I've commented on each function. 




