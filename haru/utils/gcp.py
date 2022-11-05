from google.cloud import pubsub_v1, storage

_gcs_client: storage.Client = None
_pubsub_client: pubsub_v1.PublisherClient = None


def upload_to_gcs(bucket: str, name: str, content: bytes, *, prefix: str = "") -> str:
    bucket_ = _gcs_client.get_bucket(bucket)
    blob = bucket_.blob(f"{prefix}/{name}" if prefix else name)
    blob.upload_from_string(content)
    blob.make_public()
    return blob.public_url


def publish_pubsub(topic: str, content: str):
    topic_path = _pubsub_client.topic_path("", topic)
    result = _pubsub_client.publish(topic_path, content.encode("utf-8"))
    return result.result()


def init_gcp_clients():
    global _gcs_client, _pubsub_client
    _gcs_client = storage.Client()
    _pubsub_client = pubsub_v1.PublisherClient()
