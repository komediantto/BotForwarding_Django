from django.contrib import admin
from django.utils.html import format_html

from .models import Media, Post

from .models import Channel, TargetChannel


class TargetChannelInline(admin.TabularInline):
    model = TargetChannel.channels.through
    extra = 1
    verbose_name = "Channel"
    verbose_name_plural = "Channels"


class TargetChannelAdmin(admin.ModelAdmin):
    inlines = [TargetChannelInline, ]
    exclude = ('channels',)
    list_display = ('forwarding', 'name')

    def has_add_permission(self, request):
        return True


class ChannelAdmin(admin.ModelAdmin):
    inlines = [TargetChannelInline, ]
    exclude = ('target_channels',)


admin.site.register(Channel, ChannelAdmin)
admin.site.register(TargetChannel, TargetChannelAdmin)


class MediaInline(admin.TabularInline):
    model = Media
    fields = ('file',)
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_verified',)
    search_fields = ('text',)
    list_filter = ('is_verified',)
    inlines = [MediaInline, ]


admin.site.register(Post, PostAdmin)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_media', 'post')
    search_fields = ('post',)
    list_filter = ('post',)

    def get_media_type(self, file_name):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return 'image'
        elif file_name.lower().endswith(('.mp4', '.mkv')):
            return 'video'
        else:
            return None

    def display_media(self, obj):
        if self.get_media_type(obj.file.name) == 'image':
            return format_html('<img src="{}" width="50" height="50" />',
                               obj.file.url)
        elif self.get_media_type(obj.file.name) == 'video':
            return format_html('<video width="100" height="100" controls><source src="{}" type="video/mp4"></video>',
                               obj.file.url)
        return "No media"

    display_media.short_description = 'Media'

    readonly_fields = ('display_media',)


admin.site.register(Media, MediaAdmin)
