import hashlib

from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import request


def file_upload(request: request) -> TemporaryFileUploadHandler:
    """
    It takes a file upload from a Django request and returns a TemporaryFileUploadHandler

    Args:
      request (request): request

    Returns:
      A TemporaryFileUploadHandler object.
    """

    upload = TemporaryFileUploadHandler(request)
    upload.new_file(
        request.FILES["file"].name,
        request.FILES["file"].name,
        "application/octet-stream",
        -1,
    )
    hash = hashlib.sha256()

    chunk = True
    size = 0
    while chunk:
        chunk = request.FILES["file"].read(upload.chunk_size)
        upload.receive_data_chunk(chunk, size)
        hash.update(chunk)
        size += len(chunk)
    upload.file_complete(size)

    return upload
