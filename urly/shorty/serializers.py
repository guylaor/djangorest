from rest_framework import serializers
from .models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortUrl
        fields = ('short_url', 'default_url', 'mobile_url', 'tablet_url', 'created', 'redirect_count')
