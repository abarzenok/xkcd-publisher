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


def check_vk_error(response):
    response_body = response.json()
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
    check_vk_error(upload_server)
    return upload_server.json().get['response']['upload_url']
