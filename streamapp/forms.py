# streamapp/forms.py
from django import forms

class TorrentForm(forms.Form):
    torrent_link = forms.URLField(label='Torrent Link', max_length=1000)
