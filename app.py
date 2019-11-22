from flask import Flask,render_template
import sql
app = Flask(__name__)

@app.route('/')
def hello():
    categories = sql.get_categories()
    return render_template('index.html',categories=categories)

if __name__ == '__main__':
    app.run(debug=True)