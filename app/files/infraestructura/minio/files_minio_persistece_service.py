from app.config import minio_config
from minio import Minio
import uuid

class FilesMinioPersisteceService:
    def __init__(self):
        self._minio_client = Minio(
            f"{minio_config.host}:{minio_config.port}",
            access_key=minio_config.root_user,
            secret_key=minio_config.root_password,
            secure=False,
        )
        self.bucket_name = minio_config.bucket_name

    def put_file(self, path: str) -> str:
        remote_identifier = f"{uuid.uuid4()}.pdf"
        self._minio_client.fput_object(
            self.bucket_name,
            object_name=remote_identifier,
            file_path=path,
        )
        return remote_identifier

    def get_file(self, remote_identifier: str) -> str:
        return self._minio_client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=remote_identifier,
        )