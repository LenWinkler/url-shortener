from rest_framework import serializers

from url.models import Url


class UrlSerializer(serializers.ModelSerializer):
    raw = serializers.URLField(max_length=250)
    url_hash = serializers.CharField(max_length=8)
    short = serializers.URLField()
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    def create(self, validated_data):
        url = Url.objects.create(created_by=self.context['request'].user,
                                **validated_data)
        return url

    class Meta:
        model = Url
        fields = ('raw', 'url_hash', 'short', 'created_by')
