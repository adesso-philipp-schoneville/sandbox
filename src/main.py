import os

from flask import Flask, Response, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from src.common import logger
from src.streaming_insert import stream_data
import src.errorhandling


app = Flask(__name__)
src.errorhandling.register_error_handlers(app)

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
        raise BadRequest("No Pub/Sub message received.")
    
    try:
        objectIdValue = envelope["message"]["attributes"]["objectId"]
        eventType = envelope["message"]["attributes"]["eventType"]
    except KeyError as e:
        raise src.errorhandling.RequestKeyError(f"Expected key {str(e)} not found in request.") from KeyError
    
    if ".json" not in envelope["message"]["attributes"]["objectId"]:
        raise BadRequest(f"Expected a reference to a .json file in Pub/Sub message. \
                                                Message value: \"objectId\": \"{objectIdValue}\"")
    
    if "OBJECT_FINALIZE" != eventType:
        raise src.errorhandling.RequestWrongEventType(f"Only Pub/Sub messages with the eventType \"OBJECT_FINALIZE\" are processed. \
            Message value: \"eventType\": \"{eventType}\"")
    
    # if a .json file was uploaded/edited, write its content to BigQuery
    file_path = envelope["message"]["attributes"]["objectId"]
    stream_data(file_path)

    content = "Pub/Sub message received and .json file content written to BigQuery."
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
