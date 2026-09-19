from app.config import minio_config
from minio import Minio
import uuid

class FilesMinioPersisteceService:
    def __init__(self):
        self._minio_client = Minio(
            f"{minio_config.host}:{minio_config.port}", # "minio-server:9000"
            access_key=minio_config.root_user,
            secret_key=minio_config.root_password,
            secure=False
        )
        self.backet_name = minio_config.bucket_name

    def put_file(self, path :{port}):
        remote_identifier = str(uuid.uuid4()) + ".pdf"
        self.minio_client.fput_object(
            self.backet_name,
            object_name=remote_identifier,
            file_path=path
        )
        return remote_identifier

    def get_file(self, remote_identifier):
        return self.minio_client.presigned_get_object(
            bucked_name=minio_config.bucket_name,
            object_name=remote_identifier
        )