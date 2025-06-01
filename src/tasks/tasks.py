import asyncio
import os
from random import choice, randint
from time import sleep

from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_app
from src.utils.db_manager import DBManager


@celery_app.task
def test_task() -> bool:
    sleep(randint(1, 10))
    print("Task is completed!")
    return choice([True, False])


@celery_app.task
def random_number() -> int:
    r = randint(1, 1_000_000_000)
    return r


@celery_app.task
def resize_image(image_path: str) -> None:
    sizes = [1000, 500, 200]

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resize = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )
        new_filename = f"{name}_{size}px{ext}"

        img_resize.save(os.path.join("src/static/images", new_filename))

        print("Изображение обработано")


async def get_bookings_with_today_checkin_helper():
    print("### start async get_bookings_with_today_checkin_helper")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_app.task(name="bookings_today_checkin")
def send_email2users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
