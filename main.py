import requests
from download_utils import download_image, get_file_extension_from_url


def main():
    response = requests.get('https://xkcd.com/353/info.0.json').json()
    file_name = '{}{}'.format(
        response['safe_title'],
        get_file_extension_from_url(response['img'])
    )

    download_image(
        response['img'],
        'images',
        file_name
    )


if __name__ == '__main__':
    main()
