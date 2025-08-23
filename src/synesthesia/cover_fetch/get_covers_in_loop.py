import time

from get_last_album_cover import get_last_album_cover, turn_link_into_image


def get_covers_in_loop(username: str, api_key: str):
    last_cover = None

    while True:
        try:
            current_cover = get_last_album_cover(username, api_key)

            if not current_cover:
                print("No album cover found.")
                time.sleep(10)

                continue

            if current_cover == last_cover:
                time.sleep(10)

                continue

            last_cover = current_cover
            print(current_cover)

            image = turn_link_into_image(current_cover)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(10)
