from storages.backends.s3boto3 import S3Boto3Storage
import boto3

from . import settings


class FileStorage(S3Boto3Storage):

    @property
    def connection(self):
        connection = getattr(self._connections, 'connection', None)
        if connection is None:
            session = boto3.session.Session()
            self._connections.connection = session.resource(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=settings.AWS_SESSION_TOKEN,

            )
        return self._connections.connection


class StaticStorage(FileStorage):

    location = settings.STATIC_ROOT