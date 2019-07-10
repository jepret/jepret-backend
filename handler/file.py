import os

from flask import request, g, send_file
from werkzeug.utils import secure_filename

from core.util import *
from core.error import BaseError
from model import File, User

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


def upload_file():
    if "file[]" not in request.files:
        raise BaseError("No file uploaded", 400)

    user = User.get_or_none(User.id == g.user["id"])
    if not user:
        raise BaseError("Unauthorized", 401)

    files = request.files.getlist("file[]")
    for file in files:
        if file.filename == "":
            raise BaseError("No filename uploaded", 400)

        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        if extension not in ALLOWED_EXTENSIONS:
            raise BaseError(f"{extension} not allowed", 400)

    result = []
    for file in files:
        filename = secure_filename(file.filename)
        db_file = File(filename=filename, owner=user)
        db_file.save()
        file.save(os.path.join(os.environ["UPLOAD_DIRECTORY"], db_file.unique_id))
        result.append(db_file.to_dict())

    return respond_data(result, 201)


def get_file(unique_id):
    file = File.get_or_none(File.unique_id == unique_id)
    if not file:
        raise BaseError("File not found", 404)

    extension = file.filename.split(".")[-1]
    if extension == "jpg":
        extension = "jpeg"
    mime_type = f"image/{extension}"

    return send_file(
        os.path.join(os.environ["UPLOAD_DIRECTORY"], file.unique_id), mime_type
    )
