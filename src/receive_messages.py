from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1


PROJECT_ID = "svg-dcc-sbx-generic-0516"
SUBSCRIPTION_ID = "cms-data-export-sub"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received \n{message}.")

    if ".json" in message.attributes["objectId"]:
        print(message.attributes["objectId"])

        with open("msg_data", "w") as f:
            f.write(message.data.decode())
    # message.ack()


def main():
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