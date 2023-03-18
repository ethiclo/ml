import os
from flask import Flask, request, jsonify

# Initialize flask app
server = Flask(__name__)


# Base route for testing
@server.route('/')
def healthcheck():
    """Healthcheck entrypoint.
    """
    return jsonify({'status': 200})


@server.route('/send_url/<string:url>/<string:user>', methods=["POST"])
def url(url: str, user: str) -> None:
    """Send a URL to the db.
    """
    pass

#  TODO: Make a route to classify, query, send back info to the frontend


if __name__ == '__main__':
    # Port 8080 expected by cloudrun
    # app.run(port=int(os.environ.get("PORT", 8080)),
    #         host='0.0.0.0', threaded=True)
    # app.run(host="0.0.0.0", port=8080, threaded=True)
    server.run(host="0.0.0.0", port=int(
        os.environ.get("PORT", 4000)), threaded=True)
