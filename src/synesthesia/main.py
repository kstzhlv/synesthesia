# local
from synesthesia.cover_fetch.get_last_album_cover import (
    get_last_album_cover,
    turn_link_into_image,
)
from synesthesia.cover_fetch.save_image import save_image
from synesthesia.environment_variables import API_KEY

if __name__ == "__main__":
    image_link = get_last_album_cover("codeling", API_KEY)
    img = turn_link_into_image(image_link)
    saved_image = save_image(img)
