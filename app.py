from flask import Flask,render_template
import sql
import scrap
import requests 
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def index():
    categories = scrap.category_link()
    d = dict()
    for name, path in categories.items():
        d[name] = scrap.scrap_img(path)
    return render_template('sub_cate.html',categories=categories, img_dict = d)

@app.route('/<path:name>')
def test(name):
    path = 'https://tiki.vn/' + name

    cate_nho = sql.check_category(path)

    productlist = []
    for names in cate_nho:
        a = sql.get_product(names)
        for product in a:
            productlist.append(product[0])
    
    if cate_nho:
        return render_template('product_in_category.html', productlist=productlist)

        
    else:
        categories = scrap.subcategory_link(name)
        d = dict()
        for name, path in categories.items():
            d[name] = scrap.scrap_img(path)
        return render_template('sub_cate.html', categories=categories, img_dict=d)


# @app.route('/<path:product_path>')
# def get_product(product_path):
#     return render_template('product.html', product_path=product_path)

if __name__ == '__main__':
    app.run(debug=True)


