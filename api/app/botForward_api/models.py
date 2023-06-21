from asgiref.sync import async_to_sync
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import SafeString
from dotenv import load_dotenv

from .utils import send_message

load_dotenv()


class TargetChannel(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='ID канала')
    name = models.CharField(max_length=300, verbose_name='Имя канала',
                            null=True, blank=True)
    activ = models.BooleanField(default=False, verbose_name='Включить парсинг')
    forwarding = models.BooleanField(default=False,
                                     verbose_name='Парсинг прямо в канал')

    def __str__(self) -> str:
        return self.name if self.name else str(self.telegram_id)


class Channel(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='ID канала')
    name = models.CharField(max_length=300, verbose_name='Имя канала',
                            null=True, blank=True)
    target_channels = models.ManyToManyField(TargetChannel,
                                             related_name='channels')

    def __str__(self):
        return self.name if self.name else self.telegram_id


class Post(models.Model):
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    target_channel = models.ForeignKey(TargetChannel, on_delete=models.CASCADE,
                                       related_name='posts')

    def __str__(self):
        return self.text if self.text else 'Пост без текста'


class Media(models.Model):
    file = models.FileField(upload_to='', null=True, blank=True)
    post = models.ForeignKey(Post,
                             related_name='media', on_delete=models.CASCADE)

    def __str__(self):
        link = f'<a href="{self.file.url}">Открыть</a>'
        return SafeString(link) if self.file.url else 'No Media'


class Session(models.Model):
    session_string = models.TextField(max_length=1000)


def get_media_type(file_name):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'image'
    elif file_name.lower().endswith(('.mp4', '.mkv')):
        return 'video'
    else:
        return None


@receiver(post_save, sender=Post)
def post_verified(sender, instance, update_fields, **kwargs):
    if instance.is_verified:
        session = Session.objects.first()
        medias = instance.media.all()
        media_list = [media.file.name for media in medias]
        text = instance.text
        sync_send_message = async_to_sync(send_message)
        sync_send_message(telegram_id=instance.target_channel.telegram_id,
                          text=text, media_list=media_list, session=session)
