#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request,render_template,jsonify,session,url_for
from dotenv import load_dotenv
import time

load_dotenv()

import stripe




sessions = {}
session_quantities = {}

products = {"veg":'price_1NHC2EArDOvhvxI9DypJtfRJ',"daru":'price_1NHC0jArDOvhvxI9m8eEfPg7',
            "orchard":"price_1NHC0JArDOvhvxI9vVqcmdcx","gleann oir":"price_1NHBzQArDOvhvxI9AV5jUqY6",
            "brie":"price_1NHAKhArDOvhvxI91obAKaOq","cooleeney":"price_1NHC2oArDOvhvxI9XqtmOs7Q"}



# This is your test secret API key.
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

application = Flask(__name__,static_folder="assets")
application.secret_key = "hello"

YOUR_DOMAIN = 'https://souper-fresh.com/cancel'
@application.route('/')
def home():
    return render_template("index.html")
@application.route('/shop')
def shop():
    
    
    session['user_id'] = str(int(time.time() * 1000))
    sessions[session.get("user_id")] = []

    
    quantities = {"veg":0,"daru":0,"orchard":0,"gleann oir":0,
                  "brie":0,"cooleeney":0}
    
    session_quantities[session.get("user_id")] = quantities
    print(session.get("user_id"))

    return render_template("shop.html",quantities = quantities)

@application.route('/addToCart',methods = ["POST"])
def addToCart():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    product = products[product_id]

    


    session_id = session.get("user_id")
    print(session_id)

    

    
    
    found = False
    for item in sessions[session_id]:
        if item['price'] == product:
            item['quantity']=quantity
            session_quantities[session.get("user_id")][product_id] = quantity
            found = True
    if not found:
        newProduct = {'price':product,
                      'quantity':quantity}
        
        sessions[session_id].append(newProduct)
        session_quantities[session.get("user_id")][product_id] = quantity

    print(session_quantities[session.get("user_id")])

    

    return render_template("shop.html",quantities = session_quantities[session.get("user_id")])

@application.route('/create-checkout-session', methods=['POST','GET'])
def create_checkout_session():
    shipping_line_item = {
        'price_data': {
            'currency': 'eur',
            'unit_amount': 1000,  # Amount in cents ($10 * 100)
            'product_data': {
                'name': 'Shipping',
                'description': 'Shipping charge',
            },
        },
        'quantity': 1,
    }

    
    
    session_id = session.get("user_id")
    line_items = sessions[session_id]


    line_items.append(shipping_line_item)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            
            shipping_address_collection = {
    'allowed_countries': ['IE'],  # Replace with the desired country codes
},
            mode='payment',
            success_url= url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
            payment_method_types = ["card"],
            
            
            
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@application.route('/cancel')
def cancel():
    return render_template('cancel.html')

@application.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    application.run(port=4242)