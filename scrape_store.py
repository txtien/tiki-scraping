import psycopg2
from bs4 import BeautifulSoup
from collections import deque
import requests

TIKI_URL = "https://tiki.vn"


def parse(url):
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, "html.parser")
        return response
    except Exception as err:
        print(f"Error: {err}")
        return ""

def create_categories_table():
    query = f"""CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY, 
            name VARCHAR(255), 
            url TEXt, 
            parent_id INT
            );
    """
    
    try:
        cursor.execute(query)
    except Exception as err:
        print(f"Error: {err}")

def create_products_table():
    query = f"""CREATE TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY, 
            data_id INT, 
            data_seller_id INT, 
            name VARCHAR(255), 
            price INT, 
            img TEXT, 
            cat_id INT
            );
    """
    
    try:
        cursor.execute(query)
    except Exception as err:
        print(f"Error: {err}")


class Category:
    def __init__(self, cat_id, name, url, parent_id):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id
        
    def save_into_db(self):
        query = f"""
                INSERT INTO categories(name, url, parent_id) 
                VALUES (%s, %s, %s) 
                RETURNING id;
                """
        vals = (self.name, self.url, self.parent_id)
        
        try:
            cursor.execute(query, vals)
            self.cat_id = cursor.fetchone()[0]
        except Exception as err:
            print(f"Error: {err}")
            
    def __repr__(self):
        return f"ID: {self.cat_id}, Name: {self.name}, URL: {self.url}, PARENT_ID: {self.parent_id}"

class Product:
    def __init__(self, product_id, data_id, seller_id, name, price, img, cat_id):
        self.product_id = product_id
        self.data_id = data_id 
        self.seller_id = seller_id
        self.name = name
        self.price = price
        self.img = img 
        self.cat_id = cat_id
        
    def save_into_db(self):
        query = f"""
            INSERT INTO products (data_id, data_seller_id, name, price, img, cat_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        val = (self.data_id, self.seller_id, self.name, self.price, self.img, self.cat_id)
        try:
            cursor.execute(query, val)
#             #GET ID FROM NEW ROW 
#             self.product_id = cur.fetchone()[0]
        except Exception as err:
            print(f'ERROR: {err}')
        
    def __repr__(self):
        return f'ID: {self.product_id}, Data ID: {self.data_id}, Seller ID: {self.seller_id}, Name: {self.name}, Price: {self.price}, IMG: {self.img}, Category ID: {self.cat_id}'


def get_main_categories(save_db=False):
    s = parse(TIKI_URL)
    
    category_list = []
    
    
    for i in s.findAll('a', {'class': 'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        cat_id = None
        
        name = i.find('span', {'class': 'text'}).text
        
        url = i['href'] + "&page=1"
        
        parent_id = None
        
        cat = Category(cat_id, name, url, parent_id)
        
        if save_db:
            cat.save_into_db()
            
        category_list.append(cat)
            
    return category_list

def get_sub_categories(category, save_db=False):
    name = category.name
    url = category.url
    sub_categories = []
    
    s = parse(url)
    
    try:
        div_containers = s.findAll('div',{'class': 'list-group-item is-child'})
        for div in div_containers:
            sub_id = None
            sub_name = div.a.text
            sub_url = 'https://tiki.vn' + div.a.get('href')
            sub_parent_id = category.cat_id
            
            search_text = sub_name.replace("'","''")
            cursor.execute(f"SELECT EXISTS (SELECT name FROM categories\
            WHERE name = '{search_text}')")
            result = cursor.fetchall()[0][0]
            if not result:
                cat = Category(sub_id, sub_name, sub_url, sub_parent_id)
                if save_db:
                    cat.save_into_db()
                sub_categories.append(cat)
            
    except Exception as err:
        print(f"Error: {err}")
        
    if sub_categories:
        return sub_categories
    else:
        return None
            
def get_all_categories(main_categories):
    queue = deque(main_categories)
    
    while queue:
        parent_cat = queue.popleft()
        sub_list = get_sub_categories(parent_cat,save_db=True)
        if sub_list is not None:
            queue.extend(sub_list)
        
    print('Done')


def scrape(cat, url):
    
    # Initialize empty 'results' list
    results = []

    # Run Parser on the product page
    s = parse(url)
    
    # Find all tags <div class='product-item'> and store them in 'prodct_items' list, each tag represent a product
    product_items = s.findAll('div',{'class':'product-item'})
    
    # If the tag list is empty (i.e. the page doesn't have any product), return an empty list.
    if len(product_items) == 0:
        return []

    # If the tag list is not empty (i.e. the page has products),...
    else: 
        
        # Iterate through all product and store the product information in the 'row' list
        for i in range(len(product_items)):

            row = [product_items[i]['data-id'], 
                   product_items[i]['data-seller-product-id'] if len(product_items[i]['data-seller-product-id']) != 0 else None, 
                   product_items[i]['data-title'],
                   product_items[i]['data-price'], 
                   product_items[i].find('img',{'class':'product-image img-responsive'})['src'], 
                   cat]   

            # Add the product information of each product into 'results' list
            results.append(row)
            
    # Return the list `results`   
    return results


def generate_deepest_cate_list():
    # Because category URL end with 'tree', I add '&page=1' at the end of URL so that I can generate next page easier 
    
    # With data from categories table, get all deepest categories, modify it's url to implement scrape_all function easier
    query = ('''SELECT p.url, p.id 
                FROM categories as p 
                LEFT JOIN categories as c ON c.parent_id = p.id 
                WHERE c.id IS NULL;
                ''')
    cursor.execute(query)
    deepest_cate_list = cursor.fetchall()

    for sub_cate in deepest_cate_list:
        temp = list(sub_cate)
        temp[0] += '&page=1'
        deepest_cate_list[deepest_cate_list.index(sub_cate)] = tuple(temp)
    return deepest_cate_list 

# Run scrape fuction on every page
def scrape_all(deepest_cate_list):
    print('INFO scrape_all(): Start scraping')

#   for categories in sub_cate_list:
    # Initialize 'queue' list with the results of get_urls()

    queue = deepest_cate_list 
    
    # Create table `products` if it doesn't exist yet
    # results = []  <-- This is what we did in the first week
    # While there are items in `queue`,..
    while queue:
#         print(queue)
      # `url` is set to the url of last item in `queue`
        url = queue[0][0]
      
      # `cat` is set to the category of last item in `queue`
        cat = queue[0][1]
      # Remove the last item in queue
        queue = queue[1:]

      # Run scrape(cat, url) with given `cat` and `url`
        new_rows = scrape(cat, url)
      # If the result of scrape(cat, url) is not an empty list (i.e. the page has products),...  
        if new_rows:
#             print(new_rows)
            for product in new_rows:
                id_ = None
                data_id = product[0]
                seller_id = product[1]
                name = product[2]
                price = product[3]
                img = product[4]
                cat_id = product[5]

                product = Product(id_, data_id, seller_id, name, price, img, cat_id)
                product.save_into_db()

        # Insert the result of scrape(cat, url) to table `product`
        # results += new_rows  <-- This is what we did in the first week
        #         insert_data_to_db 

        # Generate next page url 
            page = int(url[-1]) + 1
            url = url[:-1] + str(page)

    # Use this to limit our scraper to scrape only the first 10 pages of each category
    # We do this to test our scraper with a smaller task first before running through every product page
            if page < 10:
                # Add the new page url to the end of list `queue`
                queue.append((url,cat))
            query = 'SELECT COUNT(*) FROM products'
            cursor.execute(query) 
            if cursor.fetchall()[0][0] > 100000:
                print('Task completed!')
                return

def main():
    user_name = input("Your postgres username: ")
    database = input("Your database name: ")
    password = input("Your password: ")
    conn = psycopg2.connect(user = user_name,
                       database = database, password = password)
                    
    conn.autocommit = True
    global cursor
    cursor = conn.cursor()
    parse(TIKI_URL)
    create_categories_table()
    create_products_table()
    main_categories = get_main_categories(save_db=True)
    get_all_categories(main_categories)
    deepest_cate_list = generate_deepest_cate_list()
    scrape_all(deepest_cate_list)

if __name__ == '__main__':
    main()


