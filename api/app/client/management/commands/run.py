import multiprocessing

from loguru import logger

from client.handlers import media_group_handler, post_handler
from django.core.management.base import BaseCommand
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from django.core.management import execute_from_command_line

from client.config import get_or_create_session_string


def run_pyrogram():
    session = get_or_create_session_string()
    if session is None:
        pass
    else:
        client = Client('pyrogram', session_string=session.session_string)

        client.add_handler(
            MessageHandler(post_handler,
                           filters=(filters.channel) & ~(filters.media_group)))
        client.add_handler(
            MessageHandler(media_group_handler,
                           filters=[filters.channel, filters.media_group]))

        client.run()


def run_django():
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])


class Command(BaseCommand):
    help = 'Starts the Telegram client and Django server'

    def handle(self, *args, **options):
        pyrogram_process = multiprocessing.Process(target=run_pyrogram)
        django_process = multiprocessing.Process(target=run_django)

        pyrogram_process.start()
        logger.info('Pyrogram process started')
        django_process.start()
        logger.info('Django process started')

        pyrogram_process.join()
        django_process.join()
