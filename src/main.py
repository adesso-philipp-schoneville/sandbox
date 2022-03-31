import json
import os

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


@app.route("/process", methods=["POST"])
def process() -> Response:
    """
    This function is executed when the endpoint "process" was called.
    :return: Flask response
    """

    payload = request.get_json()

    # Check for required request parameters
    required_fields = ["message"]

    for param in required_fields:
        if param not in payload:
            msg = f"Required field {param} is missing in request. Request needs parameters {required_fields}"
            logger.error(msg)
            return Response(msg, 400, response_headers)

    try:
        message = payload["message"]
        message_length = len(message)

        # Create response body
        response = json.dumps(
            {
                "lengthOfMessage": message_length,
            },
            ensure_ascii=False,
        )

        return Response(response, status=200, headers=response_headers)

    except Exception as error:
        msg = "Failed to extract the message length. Error: {}".format(error)
        logger.error(msg)
        return Response(msg, status=500, headers=response_headers)


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
