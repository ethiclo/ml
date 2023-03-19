"""
Server for ethiclo
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2 as pg
from dotenv import load_dotenv
import torch

# Get the scraper
from scraper import scrape_website_text, get_imgs, sustainability_search
# Get the classification model
from models.classification.classification_classes import ResNet15, classify_img, classes

load_dotenv()

# Initialize flask app
server = Flask(__name__)
CORS(server)


# Base route for testing
@server.route('/')
def healthcheck():
    """Healthcheck entrypoint.
    """
    return jsonify({'status': 200})


@server.route('/add_shopper/<string:email>', methods=["POST"])
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


@server.route('/add_url/<string:url>/<string:email>', methods=["POST"])
def add_url(url: str, email: str):
    """Send a URL to the db.
    """

    # Connect to the db
    conn = connect()
    cur = conn.cursor()

    # Insert the url into the db
    try:
        insert = "INSERT INTO Website (url, shopper) VALUES (%s, %s);"
        cur.execute(insert, [url, email])
        conn.commit()

        # TODO: Run the model to find sustainable alternatives and add them to
        # the db.

        # Get the sustainability words and image from the URL
        # web_text = scrape_website_text(url)
        # alt_text, image = get_imgs(url)

        # # Load the classification model
        # model = ResNet15(3, len(classes))
        # model.load_state_dict(torch.load('models/classification/clothing_model_weights.pt'))
        
        # # Classify the image
        # classification = classify_img(image, model)

        # # Give it a score
        # # TODO: Add scoring model once completed
        # score = 0

        # # insert the product into the db
        # insert_product = """
        #     INSERT INTO Product (url, img_src, title, price, brand, description, score, shopper_id)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        # """
        # cur.execute(insert_product, [url, image, alt_text, 
        #                              web_text['price'], web_text['brand'], 
        #                              'description', score, email])
        # cur.commit()
    
        # # make the query
        # query = f"{classification} {alt_text.lower().replace(web_text['brand'].lower(), '')}"
        # sustainable_items = sustainability_search(query, email)

        # for item in sustainable_items:
        #     # TODO: score the item
        #     score = 0
        #     cur.execute(insert_product, [item['url'], item['img_src'], item['title'], 
        #                                  item['price'], item['brand'], 
        #                                  item['description'], score, email])
        #     cur.commit()

        cur.close()
        conn.close()
        return jsonify({'status': 200})
    except pg.Error:
        cur.close()
        conn.close()
        return jsonify({'status': 400})


@server.route('/get_sustainable_products/<string:url>/<string:user>',
              methods=["GET"])
def get_sustainable_products(url: str, user: str):
    """Fetch sustainable alternatives from the database
    """

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
        cur.execute(get_sustainable_products, [url, user])
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
    # Port 8080 expected by cloudrun
    # app.run(port=int(os.environ.get("PORT", 8080)),
    #         host='0.0.0.0', threaded=True)
    # app.run(host="0.0.0.0", port=8080, threaded=True)
    server.run(host="0.0.0.0", port=int(
        os.environ.get("PORT", 4000)), threaded=True)
    # print(os.environ)
