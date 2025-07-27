import shutil

from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    def upload_image(self, file: UploadFile):
        img_path = f"src/static/images/{file.filename}"
        with open(img_path, "wb+") as f:
            shutil.copyfileobj(file.file, f)

        resize_image.delay(img_path)  # type: ignore
