import json

from datetime import datetime
from google.cloud import storage
from google.cloud import bigquery

from src.common import logger
from src.errorhandling import BQError


DATASET_PATH = "adesso-gcc-pschville-sandbox.raw"
BUCKET_NAME = "sandbox-bucket-0"

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
    
    try:
        downloaded_blob = blob.download_as_string()
    except AttributeError:
        raise FileNotFoundError(f"The requested file was not found: {BUCKET_NAME}/{file_path}")
    
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
        raise BQError(f"Could not insert row(s) {errors}.")


def stream_data(file_path: str) -> None:
    """
    Reads file content from the given file path and writes it to BigQuery.
    """

    data = read_json_file(file_path)
    write_to_bigquery(data)
