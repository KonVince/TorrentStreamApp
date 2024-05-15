# streamapp/serializers.py
from rest_framework import serializers
from .models import Torrent
from django.core.validators import URLValidator
from .validators import validate_magnet_uri

class TorrentSerializer(serializers.ModelSerializer):
    torrent_link = serializers.CharField(max_length=1000, validators=[validate_magnet_uri])

    class Meta:
        model = Torrent
        fields = ['id', 'torrent_link', 'created_at']