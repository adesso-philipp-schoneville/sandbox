from src.common import logger
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from src.streaming_insert import stream_data


PROJECT_ID = "svg-dcc-sbx-generic-0516"
SUBSCRIPTION_ID = "cms-data-export-sub"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    logger.info(f"Received \n{message}")

    if (
        ".json" in message.attributes["objectId"]
        and "OBJECT_FINALIZE" in message.attributes["eventType"]
    ):
        file_path = message.attributes["objectId"]
        stream_data(file_path)

    message.ack()


def pull_msg():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    # Wrap subscriber in a 'with' block to automatically call close() when done.
    print(f"Listening for messages on {subscription_path}...\n")
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
        logger.info("Data streaming completed.")
