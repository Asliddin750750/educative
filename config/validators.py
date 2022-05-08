from django.utils.deconstruct import deconstructible
from rest_framework import serializers


@deconstructible
class VideoValidator:
    def __init__(self):
        pass

    def __call__(self, value):
        if str(value).split('.')[-1] != 'mp4':
            raise serializers.ValidationError('Bu video fayl emas')
