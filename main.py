import os
import random
import requests

from dotenv import load_dotenv
from pathlib import Path
from download_utils import (
    download_image,
    get_file_extension_from_url
)
from vk_utils import (
    check_vk_error,
    get_vk_photo_upload_url,
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
    Path(images_folder).mkdir(exist_ok=True)

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

    data = {
        'access_token': vk_access_token,
        'v': vk_api_version,
    }
    with open(f'{images_folder}/{file_name}', 'rb') as photo:
        files = {
            'photo': photo,
        }
        uploaded_photo = requests.post(
            upload_url,
            data=data,
            files=files,
        )
    uploaded_photo.raise_for_status()
    uploaded_photo_body = uploaded_photo.json()
    check_vk_error(uploaded_photo)
    os.remove(f'{images_folder}/{file_name}')

    data = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'group_id': vk_group_id,
        'photo': uploaded_photo_body['photo'],
        'server': uploaded_photo_body['server'],
        'hash': uploaded_photo_body['hash'],
    }
    saved_photo = requests.post(
        f'{vk_api_url}/photos.saveWallPhoto',
        data=data
    )
    saved_photo.raise_for_status()
    check_vk_error(saved_photo)
    image_id = saved_photo.json()['response'][0]['id']

    data = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': f'photo{vk_user_id}_{image_id}',
        'message': comic_alternative_text,
    }
    wall_post = requests.post(
        f'{vk_api_url}/wall.post',
        data=data
    )
    wall_post.raise_for_status()
    check_vk_error(wall_post)


if __name__ == '__main__':
    main()
