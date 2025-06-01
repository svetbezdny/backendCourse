import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("")
async def upload_image(file: UploadFile):
    img_path = f"src/static/images/{file.filename}"
    with open(img_path, "wb+") as f:
        shutil.copyfileobj(file.file, f)

    resize_image.delay(img_path)
