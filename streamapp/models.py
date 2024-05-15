# streamapp/models.py
from django.db import models
from django.core.validators import URLValidator

class Torrent(models.Model):
    torrent_link = models.CharField(max_length=1000, validators=[URLValidator(schemes=['http', 'https', 'magnet'])])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.torrent_link