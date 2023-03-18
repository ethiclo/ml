"""
Server for ethiclo
"""

import os
from flask import Flask, request, jsonify, render_template
import psycopg2 as pg
from dotenv import load_dotenv

load_dotenv()

# Initialize flask app
server = Flask(__name__)


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

    # Insert the user into the db
    try:
        insert = "INSERT INTO Shopper (email) VALUES %s"
        cur.execute(insert, [email])
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 200})
    except pg.Error:
        cur.close()
        conn.close()
        return jsonify({'status': 400})


@server.route('/send_url/<string:url>/<string:email>', methods=["POST"])
def add_url(url: str, email: str):
    """Send a URL to the db.
    """

    # Connect to the db
    conn = connect()
    cur = conn.cursor()

    # Insert the url into the db
    try:
        insert = "INSERT INTO Website (url, shopper_id) VALUES %s %s"
        cur.execute(insert, [url, email])
        conn.commit()

        # TODO: Run the model to find sustainable alternatives and add them to
        # the db.

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
        )
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
