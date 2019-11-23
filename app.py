from flask import Flask,render_template
import sql
import requests 
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def base():
    categories = sql.get_categories()
    return render_template('cate.html',categories=categories)

@app.route('/<path:name>')
def sub_cate(name):
    sub_categories = sql.get_sub_category(name)

    return render_template('sub_cate.html', sub_categories=sub_categories)

@app.route('/product/<names>')
def product(names):
    products, pages = sql.get_product(names, 0)
    same_level = sql.get_same_level_sub(names)
    return render_template('product.html', products=products, names=names, pages=pages, same_level=same_level)

@app.route('/product/<names>/<int:command>')
def analysis(names, command):
    if isinstance(command, int):
        products, pages = sql.get_product(names, int(command))
        same_level = sql.get_same_level_sub(names)

    return render_template('product.html', products=products, names=names, pages=pages, same_level=same_level)


# @app.route('/product/<path:page>')
# def page(page):
#     pass

# @app.route('/<path:product_path>')
# def get_product(product_path):
#     return render_template('product.html', product_path=product_path)

if __name__ == '__main__':
    app.run(debug=True)


