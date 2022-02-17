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
