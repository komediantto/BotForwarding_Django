from loguru import logger
from pyrogram import Client, types

from client.interface import interface
from client.utils import create_data_for_api, get_channels, send_to_channel

media_group_chats = set()


def post_handler(client: Client, message: types.Message):
    '''Ловим сообщения без прикреплений, либо с одним прикреплением'''
    target_channels = get_channels()
    logger.warning(target_channels)
    for target in target_channels:
        if message.chat.id in \
           [int(channel.telegram_id) for channel in target.channels.all()]:
            if target.forwarding:
                send_to_channel(client, message, target)
            else:
                data = create_data_for_api(message, client, target)
                if interface.send_post(data=data):
                    logger.debug('Успех')
                else:
                    logger.debug('Провал')


def media_group_handler(client: Client, message: types.Message):
    '''Ловим медиагруппы'''
    target_channels = get_channels()
    logger.warning(target_channels)
    channels = []
    for target in target_channels:
        channels += [int(
            channel.telegram_id) for channel in target.channels.all()]

    if message.chat.id not in channels or message.chat.id in media_group_chats:
        return

    media_group_chats.add(message.chat.id)

    for target in target_channels:
        if target.forwarding:
            send_to_channel(client, message, target, media_group=True)

        else:
            data = create_data_for_api(message, client,
                                       target, media_group=True)
            if interface.send_post(data=data):
                logger.warning('Успех')
            else:
                logger.warning('Провал')
        media_group_chats.clear()
