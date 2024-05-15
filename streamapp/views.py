from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Torrent
from .serializers import TorrentSerializer
from .forms import TorrentForm
from rest_framework import status

class TorrentViewSet(viewsets.ModelViewSet):
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer

@api_view(['GET', 'POST'])
def torrent_list(request):
    if request.method == 'GET':
        torrents = Torrent.objects.all()
        serializer = TorrentSerializer(torrents, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TorrentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def upload_torrent(request):
    if request.method == 'POST':
        form = TorrentForm(request.POST)
        if form.is_valid():
            torrent_link = form.cleaned_data['torrent_link']
            Torrent.objects.create(torrent_link=torrent_link)
            return redirect('success')
    else:
        form = TorrentForm()
    return render(request, 'upload_torrent.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def home(request):
    return render(request, 'home.html')
