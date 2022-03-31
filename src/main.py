import json
import os
import receive_messages
import read_storage

from flask import Flask, Response, request
from flask_cors import CORS

from src.common import logger

app = Flask(__name__)

# Set CORS headers for the preflight request
CORS(app)

# Set response header
response_headers = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}


@app.route("/pull-messages", methods=["POST"])
def pull_messages() -> Response:
    try:
        receive_messages.main()
    except Exception as err:
        msg = f"Error {err}"
        logger.error(msg)

    content = "Finished pulling messages."
    return Response(content, status=200, headers=response_headers)


@app.route("/read-storage", methods=["POST"])
def read_object() -> Response:
    read_storage.main()
    content = "Finished reading objects."
    return Response(content, status=200, headers=response_headers)


if __name__ == "__main__":
    """
    Start Flask in Cloud Run Container.
    """

    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        use_reloader=False,
    )
