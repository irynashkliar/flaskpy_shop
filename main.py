from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)


@app.route('/')
def home():
    items = Item.query.order_by(Item.price).all()
    return render_template('home.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/returns')
def returns():
    return render_template('returns.html')


@app.route('/affiliatepr')
def affiliatepr():
    return render_template('affiliatepr.html')


@app.route('/careers')
def careers():
    return render_template('careers.html')


@app.route('/shipping')
def shipping():
    return render_template('shipping.html')


@app.route('/buy')
def item_buy(id):

    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "error"

    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
