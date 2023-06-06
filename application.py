#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request,render_template,jsonify
from dotenv import load_dotenv

load_dotenv()

import stripe


products = {"veg":'price_1NAMzjArDOvhvxI9l7GVv3N7',"daru":'price_1NCXIAArDOvhvxI9Lko5dXy8',
            "orchard":"price_1NCXTuArDOvhvxI9zwJQOkRt","gleann oir":"price_1NCXUjArDOvhvxI93b7wUpBc",
            "brie":"price_1NFkbKArDOvhvxI94MxYTFdC","cooleeney":"price_1NFkcOArDOvhvxI9eUCqGA9A"}
line_items = []
# This is your test secret API key.
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

application = Flask(__name__,static_folder="assets")

YOUR_DOMAIN = 'http://localhost:4242'
@application.route('/')
def home():
    return render_template("index.html")
@application.route('/shop')
def shop():
    return render_template("shop.html")

@application.route('/addToCart',methods = ["POST"])
def addToCart():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    product = products[product_id]
    found = False
    for item in line_items:
        if item['price'] == product:
            item['quantity']+=quantity
            found = True
    if not found:
        newProduct = {'price':product,
                      'quantity':quantity}
        line_items.append(newProduct)

    return render_template("shop.html")

@application.route('/create-checkout-session', methods=['POST','GET'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            
            shipping_address_collection = {
    'allowed_countries': ['IE'],  # Replace with the desired country codes
},
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            payment_method_types = ["card"],
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    application.run(port=4242)