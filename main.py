import os
import random
import requests
from dotenv import load_dotenv
from pathlib import Path
from requests import HTTPError
from download_utils import (
    download_image,
    get_file_extension_from_url,
)
from vk_utils import (
    VKError,
    get_vk_photo_upload_url,
    upload_photo_to_vk,
    save_vk_wall_photo,
    post_to_vk_wall,
)


def get_random_xkcd_comic():
    last_comic = requests.get('https://xkcd.com/info.0.json')
    last_comic.raise_for_status()
    total_comics = last_comic.json()['num']
    random_comic_number = random.randint(1, total_comics)
    random_comic = requests.get(
        f'https://xkcd.com/{random_comic_number}/info.0.json'
    )
    random_comic.raise_for_status()
    return random_comic.json()


def main():
    load_dotenv()

    vk_api_version = 5.131
    vk_access_token = os.getenv('VK_API_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_user_id = os.getenv('VK_USER_ID')

    images_folder = 'images'
    file_name = None
    Path(images_folder).mkdir(exist_ok=True)

    try:
        xkcd_comic = get_random_xkcd_comic()
        comic_alternative_text = xkcd_comic['alt']
        file_name = '{}{}'.format(
            xkcd_comic['safe_title'],
            get_file_extension_from_url(xkcd_comic['img'])
        )
        download_image(
            xkcd_comic['img'],
            images_folder,
            file_name
        )
        upload_url = get_vk_photo_upload_url(
            vk_access_token,
            vk_api_version,
            vk_group_id
        )

        with open(f'{images_folder}/{file_name}', 'rb') as photo:
            uploaded_photo_body = upload_photo_to_vk(
                vk_access_token,
                vk_api_version,
                upload_url,
                photo
            )
        image_id = save_vk_wall_photo(
            vk_access_token,
            vk_api_version,
            vk_group_id,
            uploaded_photo_body['photo'],
            uploaded_photo_body['server'],
            uploaded_photo_body['hash']
        )['response'][0]['id']

        post_to_vk_wall(
            vk_access_token,
            vk_api_version,
            vk_group_id,
            vk_user_id,
            image_id,
            comic_alternative_text
        )
    except VKError as vk_err:
        print(
            'VK returned an error.',
            vk_err.__str__(),
            sep='\n'
        )
    except HTTPError as http_err:
        print(
            'HTTP error occurred.',
            http_err.__str__(),
            sep='\n'
        )
    finally:
        Path(f'{images_folder}/{file_name}').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
