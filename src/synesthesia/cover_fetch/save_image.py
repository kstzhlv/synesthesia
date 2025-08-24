# standard
import os

# third party
from PIL import Image

PATH = "/tmp/covers/"


def save_image(img: Image.Image) -> str:
    if not os.path.exists(PATH):
        os.mkdir(PATH)

    result_path = os.path.join(PATH, "album_cover.jpg")

    img.save(result_path)

    return result_path
