import os
import random
import requests
from download_utils import download_image, get_file_extension_from_url
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint # debug only


def main():
    load_dotenv()

    images_folder = 'images'
    Path(images_folder).mkdir(exist_ok=True)

    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    total_comics = response.json()['num']
    random_comic_number = random.randint(1, total_comics)

    response = requests.get(f'https://xkcd.com/{random_comic_number}/info.0.json')
    response.raise_for_status()
    file_name = '{}{}'.format(
        response.json()['safe_title'],
        get_file_extension_from_url(response.json()['img'])
    )

    download_image(
        response.json()['img'],
        images_folder,
        file_name
    )

    alt = response.json()['alt'] # rename
    print(alt)

    params = {
        'access_token': os.getenv('VK_API_ACCESS_TOKEN'),
        'v': 5.131,
    }
    vk_response = requests.get(
        'https://api.vk.com/method/groups.get',
        params=params
    )
    vk_response.raise_for_status()
    pprint(vk_response.json())

    params['group_id'] = 210688801

    vk_response = requests.get(
        'https://api.vk.com/method/photos.getWallUploadServer',
        params=params
    )
    vk_response.raise_for_status()
    pprint(vk_response.json())
    upload_url = vk_response.json()['response']['upload_url']
    print(upload_url)

    data = {
        'access_token': os.getenv('VK_API_ACCESS_TOKEN'),
        'v': 5.131,
    }
    with open(f'{images_folder}/{file_name}', 'rb') as photo:

        files = {
            'photo': photo,
        }

        vk_response = requests.post(
            upload_url,
            data=data,
            files=files,
        )
        vk_response.raise_for_status()
        pprint(vk_response.json())
    params['photo'] = vk_response.json()['photo']
    params['server'] = vk_response.json()['server']
    params['hash'] = vk_response.json()['hash']

    os.remove(f'{images_folder}/{file_name}')

    vk_response = requests.post(
        'https://api.vk.com/method/photos.saveWallPhoto',
        data=params
    )
    vk_response.raise_for_status()
    pprint(vk_response.json())

    image_id = vk_response.json()['response'][0]['id']

    data = {
        'access_token': os.getenv('VK_API_ACCESS_TOKEN'),
        'v': 5.131,
        'owner_id': -210688801,
        'from_group': 1,
        'attachments': f'photo6166300_{image_id}',
        'message': alt,
    }
    vk_response = requests.post(
        'https://api.vk.com/method/wall.post',
        data=data
    )
    vk_response.raise_for_status()
    pprint(vk_response.json())


if __name__ == '__main__':
    main()
