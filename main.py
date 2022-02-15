import os
import random
import requests
from download_utils import download_image, get_file_extension_from_url
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint # debug only


def main():
    load_dotenv()
    vk_api_url = 'https://api.vk.com/method/'
    vk_api_version = 5.131
    vk_access_token = os.getenv('VK_API_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_user_id = os.getenv('VK_USER_ID')
    images_folder = 'images'
    Path(images_folder).mkdir(exist_ok=True)

    last_comic = requests.get('https://xkcd.com/info.0.json')
    last_comic.raise_for_status()
    total_comics = last_comic.json()['num']
    random_comic_number = random.randint(1, total_comics)

    random_comic = requests.get(f'https://xkcd.com/{random_comic_number}/info.0.json')
    random_comic.raise_for_status()
    comic_alternative_text = random_comic.json()['alt']
    file_name = '{}{}'.format(
        random_comic.json()['safe_title'],
        get_file_extension_from_url(random_comic.json()['img'])
    )
    download_image(
        random_comic.json()['img'],
        images_folder,
        file_name
    )

    params = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'group_id': vk_group_id,
    }
    upload_server = requests.get(
        f'{vk_api_url}/photos.getWallUploadServer',
        params=params
    )
    upload_server.raise_for_status()
    upload_url = upload_server.json()['response']['upload_url']

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
    os.remove(f'{images_folder}/{file_name}')

    data = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'group_id': vk_group_id,
        'photo': uploaded_photo.json()['photo'],
        'server': uploaded_photo.json()['server'],
        'hash': uploaded_photo.json()['hash'],
    }
    saved_photo = requests.post(
        f'{vk_api_url}/photos.saveWallPhoto',
        data=data
    )
    saved_photo.raise_for_status()
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
    pprint(wall_post.json())


if __name__ == '__main__':
    main()
