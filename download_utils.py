import os
from urllib import parse
import requests


def get_file_extension_from_url(url):
    """Get extension of a file and return it as str (e.g. '.jpg')"""
    unquoted_url_path = parse.unquote(parse.urlsplit(url).path)
    file_name = os.path.split(unquoted_url_path)[-1]
    return os.path.splitext(file_name)[-1]


def download_image(image_url, image_dir, image_name, params=None):
    """Download image to specified directory and return None."""
    full_path = os.path.join(image_dir, image_name)

    response = requests.get(image_url, params=params)
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)