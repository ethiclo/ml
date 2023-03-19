"""
Server for ethiclo
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2 as pg
from dotenv import load_dotenv
from helpers import handle_url
from scraper import sustainability_search

load_dotenv()

# Initialize flask app
app = Flask(__name__)
CORS(app)


# Base route for testing
@app.route('/')
def healthcheck():
    """Healthcheck entrypoint.
    """
    return jsonify({'status': 200})


@app.route('/add_shopper/<string:email>', methods=["POST"])
def add_shopper(email: str):
    """Add a shopper to the db.
    """
    # Connect to the db
    conn = connect()
    cur = conn.cursor()
    print("Connected to db")

    # Insert the user into the db
    try:
        insert = "INSERT INTO Shopper (email) VALUES (%s)"
        cur.execute(insert, [email])
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 200})
    except pg.Error:
        cur.close()
        conn.close()
        return jsonify({'status': 400, 'error': pg.Error})


@app.route('/add_url', methods=["POST"])
def add_url():
    """Send a URL to the db.
    """
    # Get the data from the request
    data = request.get_json()
    url = data['url']
    email = data['email']
    # Connect to the db
    conn = connect()
    cur = conn.cursor()

    # Insert the url into the db
    try:
        insert = "INSERT INTO Website (url, shopper) VALUES (%s, %s);"
        cur.execute(insert, [url, email])
        conn.commit()

        # TODO: Call helper function

        data = handle_url(url)

        # insert the product into the db
        insert_product = """
            INSERT INTO Product (url, img_src, title, price, brand, description, score, shopper)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_product, [data['url'], data['image'], data['title'], 
                                     data['price'], data['brand'], 
                                     'description', data['score'], email])
        cur.commit()
    
        # make the query
        query = f"{data['classification']} {data['title'].lower().replace(data['brand'].lower(), '')}"
        sustainable_items = sustainability_search(query, email)

        for item in sustainable_items:
            # TODO: score the item
            score = 0
            cur.execute(insert_product, [item['url'], item['img_src'], item['title'], 
                                         item['price'], item['brand'], 
                                         item['description'], score, email])
            cur.commit()

        cur.close()
        conn.close()
        return jsonify({'status': 200})
    except pg.Error:
        cur.close()
        conn.close()
        return jsonify({'status': 400})


@app.route('/get_sustainable_products', methods=["GET"])
def get_sustainable_products():
    """Fetch sustainable alternatives from the database
    """
    data = request.get_json()
    url = data['url']
    email = data['email']

    # Get the sustainable alternatives from the db
    get_sustainable_products = """
        SELECT * FROM Product
        WHERE alt_to IN (
            SELECT product_id FROM Product
            WHERE url = %s AND shopper_id = %s
        );
    """
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(get_sustainable_products, [url, email])
        products = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'status': 200, 'products': products})
    except pg.Error:
        cur.close()
        conn.close()
        return jsonify({'status': 400})


def connect():
    """Connect to the db.
    """
    try:
        connection = pg.connect(
            dbname=os.environ["PGDATABASE"], user=os.environ["PGUSER"],
            password=os.environ["PASSWORD"],
            options="-c search_path=ethiclo"
        )
        return connection
    except pg.Error:
        return None


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
