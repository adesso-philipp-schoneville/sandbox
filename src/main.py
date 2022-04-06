import os

from flask import Flask, Response, request
from flask_cors import CORS

from src.common import logger
from src.streaming_insert import stream_data


app = Flask(__name__)

# Set CORS headers for the preflight request
CORS(app)

# Set response header
response_headers = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}


@app.route("/get-messages", methods=["POST"])
def get_messages() -> Response:
    """
    Get all messages from a pub/sub topic and loads the content of a JSON file into a
    BigQuery table.
    """

    envelope = request.get_json()

    if not envelope:
        msg = "No Pub/Sub message received."
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if (
        ".json" in envelope["message"]["attributes"]["objectId"]
        and "OBJECT_FINALIZE" in envelope["message"]["attributes"]["eventType"]
    ):
        file_path = envelope["message"]["attributes"]["objectId"]
        stream_data(file_path)

    content = "Pub/Sub message received."
    logger.info(content)
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
