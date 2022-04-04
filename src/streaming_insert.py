from google.cloud import storage
from google.cloud import bigquery
from src.common import logger
import json
from datetime import datetime


DATASET_PATH = "svg-dcc-sbx-generic-0516.raw"
BUCKET_NAME = "cms-data-export-c46f0c99"
STORAGE_CLIENT = storage.Client()
BQ_CLIENT = bigquery.Client()


def read_json_file(file_path: str) -> dict:
    """
    Reads a file path for a JSON object from the storage bucket and converts into a dict.
    :param: Storage file path
    :return: Dictionary with file content
    """

    file_category = file_path.split("/")[0]
    file_data = {}
    file_data[file_category] = {}

    bucket = STORAGE_CLIENT.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob(f"{file_path}")
    downloaded_blob = blob.download_as_string()
    data = json.loads(downloaded_blob)
    data.setdefault("ingestion_time", str(datetime.now()))
    file_data[file_category].update(data)

    return file_data


def write_to_bigquery(document: dict) -> None:
    """
    Function that writes document as row to BigQuery.
    :param document: JSON file
    :param table_id: GCP table id
    :return: None
    """

    table_name = list(document.keys())[0]
    table_id = ".".join([DATASET_PATH, table_name])

    rows_to_insert = []
    rows_to_insert.append(document[table_name])

    errors = BQ_CLIENT.insert_rows_json(table_id, rows_to_insert)
    if errors:
        logger.error(f"Could not insert row {errors}.")
        raise Exception(errors)


def stream_data(file_path: str) -> None:
    data = read_json_file(file_path)
    write_to_bigquery(data)
