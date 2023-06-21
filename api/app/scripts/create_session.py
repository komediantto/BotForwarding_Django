import os
from pyrogram import Client
from botForward_api.models import Session
from loguru import logger


def run():
    with Client('pyroclient',
                os.getenv('API_ID'), os.getenv('API_HASH')) as client:
        session_string = client.export_session_string()

    Session.objects.create(session_string=session_string)
    logger.warning('Сессия успешно создана')
