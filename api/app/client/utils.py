from typing import List, Optional, Union

from loguru import logger
from pyrogram import types, Client
from botForward_api.models import TargetChannel

from .exceptions import EmptyTargetError


def get_channels() -> List[TargetChannel]:
    '''Получение таргет-каналов'''
    target_channels = TargetChannel.objects.all()
    if target_channels is None:
        raise EmptyTargetError

    return target_channels


def generate_telegram_files(media_messages: List[types.Message]) -> \
                                List[Union[types.InputMediaPhoto,
                                           types.InputMediaVideo]]:
    '''Генерирует список из телеграм файлов'''
    media_list = []
    for media in media_messages:
        if media.photo:
            if media.caption:
                media_list.append(
                    types.InputMediaPhoto(media.photo.file_id,
                                          caption=media.caption.markdown))
            else:
                media_list.append(types.InputMediaPhoto(media.photo.file_id))
        elif media.video:
            if media.caption:
                media_list.append(
                    types.InputMediaVideo(media.video.file_id,
                                          caption=media.caption.markdown))
            else:
                media_list.append(types.InputMediaVideo(media.video.file_id))
    return media_list


def send_only_one_attachment(client: Client, message: types.Message,
                             target: TargetChannel) -> None:
    '''Отправляет пустое сообщение, либо сообщение с одним файлом'''
    if message.photo:
        try:
            client.send_photo(chat_id=int(target.telegram_id),
                              photo=message.photo.file_id,
                              caption=message.caption.markdown)
        except AttributeError:
            client.send_photo(chat_id=int(target.telegram_id),
                              photo=message.photo.file_id)
    elif message.video:
        client.send_video(chat_id=int(target.telegram_id),
                          video=message.video.file_id,
                          caption=message.caption.markdown)
    else:
        client.send_message(chat_id=int(target.telegram_id),
                            text=message.text.markdown)


def send_to_channel(client: Client,
                    message: types.Message, target: TargetChannel,
                    media_group=False):
    '''Пересылка сообщения в таргет-канал'''
    if media_group:
        media_group_messages = client.get_media_group(
            chat_id=message.chat.id,
            message_id=message.id)
        media = generate_telegram_files(media_group_messages)
        client.send_media_group(chat_id=int(target.telegram_id),
                                media=media)
    else:
        send_only_one_attachment(client, message, target)


def create_data_for_api(message: types.Message,
                        client: Client, target: TargetChannel,
                        media_group=False):
    files: List[str] = list()
    text: Optional[str] = None
    if media_group:
        data = with_media_group(client, message, target, files)
    else:
        if message.photo or message.video:
            media = client.download_media(message, 'media/')
            files.append(media)
        if message.caption:
            text = message.caption.markdown if hasattr(
                message.caption, 'markdown') else None
        elif message.text:
            text = message.text.markdown if hasattr(
                message.text, 'markdown') else None
        data = {
            'text': text,
            'media': files,
            'target_channel': target.id
                    }
    return data


def with_media_group(client: Client, message: types.Message,
                     target: TargetChannel, files: list):
    media_group_messages = client.get_media_group(
        chat_id=message.chat.id, message_id=message.id)
    for media_message in media_group_messages:
        media = client.download_media(media_message, 'media/')
        files.append(media)
        if media_message.caption:
            text = media_message.caption.markdown

    data = {'text': text,
            'media': files,
            'target_channel': target.id
            }
    logger.warning(data)
    return data
