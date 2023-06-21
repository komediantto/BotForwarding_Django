import os
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Post, Media
from .serializers import PostSerializer
from loguru import logger


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid():
            post = post_serializer.save()
            media_files = request.POST.getlist('media')
            logger.warning(media_files)

            for media_file in media_files:
                file_name = os.path.basename(media_file)
                media = Media(file=file_name, post=post)
                media.save()

            return Response(post_serializer.data)

        return Response(post_serializer.errors)
