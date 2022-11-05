from google.cloud import storage

_gcs_client: storage.Client = None


def upload_to_gcs(bucket: str, name: str, content: bytes, *, prefix: str = "") -> str:
    bucket_ = _gcs_client.get_bucket(bucket)
    blob = bucket_.blob(f"{prefix}/{name}" if prefix else name)
    blob.upload_from_string(content)
    blob.make_public()
    return blob.public_url


def init_gcp_clients():
    global _gcs_client
    _gcs_client = storage.Client()
