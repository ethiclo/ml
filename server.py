"""
Server for ethiclo
"""

import os
from flask import Flask, request, jsonify
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


@server.route('/send_url/<string:url>/<string:user>', methods=["POST"])
def add_url(url: str, user: str) -> None:
    """Send a URL to the db.
    """

    # Connect to the db
    conn = connect()
    cur = conn.cursor()


@server.route('/get_url/<string:user>', methods=["GET"])
def get_url(user: str) -> None:
    """Get a url for user from the database
    """


@server.route('/get_sustainable_products/<string:url>/<string:user>',
              methods=["GET"])
def get_sustainable_products(url: str, user: str) -> None:
    """Fetch sustainable alternatives from the database
    """


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
