from flask import Flask,render_template, request
import sql
import requests 
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def index():
    # Page for 16 1st categories 
    categories = sql.get_categories()
    return render_template('cate.html',categories=categories)

@app.route('/<path:name>')
def sub_cate(name):
    # Page for sub of each 1st category
    sub_categories = sql.get_sub_category(name)

    return render_template('sub_cate.html', names = name, sub_categories=sub_categories)

@app.route('/product/<names>')
def product(names):
    # Page for products of each sub category, display 12 products
    products, pages = sql.get_product(names, 0)
    same_level = sql.get_same_level_sub(names)
    return render_template('product.html', products=products, names=names, pages=pages, same_level=same_level)

@app.route('/product/<names>/<command>')
def pages(names, command):
    # Display another page of one products (number of pages depend on number of products), OR display the result after sort by price 
    try:
        if isinstance(int(command), int):
            products, pages = sql.get_product(names, int(command))
            same_level = sql.get_same_level_sub(names)
    except:
        products, pages = sql.get_product(names, 0, command=command)
        same_level = sql.get_same_level_sub(names)

    return render_template('product.html', products=products, names=names, pages=pages, same_level=same_level)

@app.route('/product/<names>/search')
def product_search(names):
    # Make search function for search bar
    keyword = request.args.get('search')
    products, pages = sql.filter_product(keyword,0, name=names)

    return render_template('filter_product.html', products=products, names=names, pages=pages, keyword=keyword)

@app.route('/product/<names>/<keyword>/<page>')
def product_searchpage(names,keyword, page):
    # Make page for products after doing search, OR the result when after by price (apply on searched products)
    try:
        if isinstance(int(page), int):
            products, pages = sql.filter_product(keyword, int(page), name=names)
    except:
        products, pages = sql.filter_product(keyword, 0, name=names, command=page)

    return render_template('filter_product.html', products=products, names=names, pages=pages, keyword=keyword)


if __name__ == '__main__':
    app.run(debug=True)


