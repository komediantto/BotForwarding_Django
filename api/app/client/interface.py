import requests
from loguru import logger


class Interface():
    posts_url = "http://localhost:8000/api/posts/"

    def send_post(self, data):
        response = requests.post(self.posts_url, data=data)
        try:
            logger.warning(response.json())
        except requests.exceptions.JSONDecodeError as e:
            logger.warning(f"JSONDecodeError: {e}")
            return False

        if response.status_code == 200 or response.status_code == 201:
            return True

    def get_post(self, data, url):
        response = requests.post(url,
                                 data=data)
        try:
            logger.warning(response.json())
        except requests.exceptions.JSONDecodeError as e:
            logger.warning(f"JSONDecodeError: {e}")
            return False

        if response.status_code == 200 or response.status_code == 201:
            return True


interface = Interface()
