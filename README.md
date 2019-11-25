# 1. Project Name
- Web Crawler

# 2. Description
- Crawl 10 pages from each category in Tiki and store the data in Postgresql database. Then make some general analysis about Tiki.

# 3. Installation
- You need to install Python, Flask, Postgresql, psycopg2, BeautifulSoup, Anaconda


# 4. Guide
1. Log in your Postgresql user (say "your_username") and create a new database (say "your_db_name")

2. Open scrape_store.py, at line 8 , change 

`conn = psycopg2.connect( user = "{your_username}",database = "{your_db_name"}, password = "{your__postgres_password})"`

3. Crawl 10 pages from each category in Tiki and store the data in Postgresql database
- Run scrape_store.py file in Terminal :`python scrape_store.py`

4. Now you have 2 tables : 'categories' and 'products'
- See its schema in Postgres

5. Run `app.py` , open your browser, type your localhost address and explore
 




