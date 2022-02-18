import requests

VK_API_URL = 'https://api.vk.com/method/'


class VKError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self, message)

    def __str__(self):
        return f'Error code: {self.code}\n' \
               f'Error message: {self.message}'


def check_vk_error(response_body):
    if response_body.get('error'):
        raise VKError(
            response_body.get('error').get('error_code'),
            response_body.get('error').get('error_msg')
        )


def get_vk_photo_upload_url(
        access_token,
        api_version,
        group_id
):
    params = {
        'access_token': access_token,
        'v': api_version,
        'group_id': group_id,
    }
    upload_server = requests.get(
        f'{VK_API_URL}/photos.getWallUploadServer',
        params=params
    )
    upload_server.raise_for_status()
    upload_server_body = upload_server.json()
    check_vk_error(upload_server_body)
    return upload_server_body['response']['upload_url']


def upload_photo_to_vk(
        access_token,
        api_version,
        upload_url,
        photo
):
    data = {
        'access_token': access_token,
        'v': api_version,
    }
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
    check_vk_error(uploaded_photo_body)
    return uploaded_photo_body


def save_vk_wall_photo(
        access_token,
        api_version,
        group_id,
        vk_photo,
        vk_server,
        vk_photo_hash
):
    data = {
        'access_token': access_token,
        'v': api_version,
        'group_id': group_id,
        'photo': vk_photo,
        'server': vk_server,
        'hash': vk_photo_hash,
    }
    saved_photo = requests.post(
        f'{VK_API_URL}/photos.saveWallPhoto',
        data=data
    )
    saved_photo.raise_for_status()
    saved_photo_body = saved_photo.json()
    check_vk_error(saved_photo_body)
    return saved_photo_body


def post_to_vk_wall(
        access_token,
        api_version,
        vk_group_id,
        vk_user_id,
        image_id,
        post_text
):
    data = {
        'access_token': access_token,
        'v': api_version,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': f'photo{vk_user_id}_{image_id}',
        'message': post_text,
    }
    wall_post = requests.post(
        f'{VK_API_URL}/wall.post',
        data=data
    )
    wall_post.raise_for_status()
    wall_post_body = wall_post.json()
    check_vk_error(wall_post_body)
    return wall_post_body
