import os
from src.receive_messages import pull_msg
from flask import Flask, Response
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
    """
    Pulls all messages from a pub/sub topic and loads the content of a JSON file into a
    BigQuery table.
    """

    try:
        pull_msg()
    except Exception as err:
        msg = f"Error {err}"
        logger.error(msg)

    content = "Finished pulling messages."
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
