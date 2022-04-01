from google.cloud import storage
from google.cloud import tasks_v2
from src.common import logger
import json
import datetime


GCP_PROJECT = "noz-digital-audio-data-dev"
LOCATION = "europe-west3"
BUCKET_NAME = "cms-data-export-c46f0c99"
# TODO: Change task queue name
TASK_QUEUE = "extract-app-queue"

STORAGE_CLIENT = storage.Client()
TASK_CLIENT = tasks_v2.CloudTasksClient()
PARENT = TASK_CLIENT.queue_path(GCP_PROJECT, LOCATION, TASK_QUEUE)


dispatch_config = {
    "location": "europe-west3",
    "method": tasks_v2.HttpMethod.POST,
    # TODO: Change URL path
    "url": "https://bq-transformer-6jbndwjyvq-ey.a.run.app/transform",
    "headers": {"Content-type": "application/json"},
    # TODO: Change service account
    "account": "sa-extract-app@noz-digital-audio-data-dev.iam.gserviceaccount.com",
}


def read_json_file(file_path: str) -> json:
    """
    Reads a file path from the storage bucket and converts it to a JSON file.
    :param: Storage file path
    :return: JSON object
    """

    bucket = STORAGE_CLIENT.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob(f"{file_path}")
    downloaded_blob = blob.download_as_string()
    data = json.loads(downloaded_blob)
    data["ingestion_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = json.dumps(data)
    return json_data


def create_task_with_data(data: json) -> tasks_v2.Task:
    """
    Push content of a file to Cloud Tasks Queue.
    :param data:
    """

    task = {
        "http_request": {  # Specify the type of request.
            "http_method": dispatch_config["method"],
            "url": dispatch_config["url"],
            "headers": dispatch_config["headers"],
            "oidc_token": {"service_account_email": dispatch_config["account"]},
            "body": data.encode("utf-8"),
        }
    }
    try:
        TASK_CLIENT.create_task(request={"parent": PARENT, "task": task})
    except Exception as e:
        reason = (
            f"create_task Exception, An error occurred while creating the Task: {e}"
        )
        logger.error(reason)
        raise e


def main(file_path):
    data = read_json_file(file_path)
    create_task_with_data(data)
