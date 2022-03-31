from google.cloud import storage


def main():
    client = storage.Client()
    bucket = client.get_bucket("cms-data-export-c46f0c99")
    blob = bucket.get_blob("articles/hello.txt")
    downloaded_blob = blob.download_as_string()
    print(downloaded_blob)
