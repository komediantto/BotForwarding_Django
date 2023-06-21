from dotenv import load_dotenv
from loguru import logger
from typing import List
from pyrogram import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo


load_dotenv()


async def send_message(telegram_id, text, media_list, session):
    async with Client('djangoclient',
                      session_string=session.session_string) as client:

        if len(media_list) > 1:
            await create_and_send_media_group(media_list, text,
                                              client, telegram_id)
        elif len(media_list) == 1:
            await send_single_file(media_list, text, client, telegram_id)
        else:
            await client.send_message(telegram_id, text)


async def create_and_send_media_group(media_list: List[str], text: str,
                                      client: Client, telegram_id: int):
    '''Создание и отправление медиагруппы с caption'''
    input_files = []
    for i, media in enumerate(media_list):
        if get_media_type(media) == 'image':
            if i == 0:
                input_files.append(
                    InputMediaPhoto(f'../media/{media}',
                                    caption=text))
            else:
                input_files.append(
                    InputMediaPhoto(f'../media/{media}'))
        elif get_media_type(media) == 'video':
            if i == 0:
                input_files.append(
                    InputMediaVideo(f'../media/{media}', caption=text))
            else:
                input_files.append(
                    InputMediaVideo(f'../media/{media}'))
    await client.send_media_group(telegram_id, input_files)
    logger.debug('Отправлено')


async def send_single_file(media_list: List[str], text: str,
                           client: Client, telegram_id: int):
    '''Отправка одиночного файла с caption'''
    if get_media_type(media_list[0]) == 'image':
        await client.send_photo(
            telegram_id,
            f'app/media/{media_list[0]}',
            text)
    elif get_media_type(media_list[0]) == 'video':
        await client.send_video(
            telegram_id, f'app/media/{media_list[0]}', text)


def get_media_type(file_name: str):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'image'
    elif file_name.lower().endswith(('.mp4', '.mkv')):
        return 'video'
    else:
        return None
