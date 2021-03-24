from rest_framework import serializers

from .models import Url


class UrlSerializer(serializers.ModelSerializer):
    raw = serializers.URLField(max_length=250)
    url_hash = serializers.CharField(max_length=8)
    short = serializers.URLField()

    class Meta:
        model = Url
        fields = '__all__'
