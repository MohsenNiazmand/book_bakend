from rest_framework import viewsets
from .models import Reciter, ChapterAudio, AudioTimestamp
from .serializers import (
    ReciterSerializer, 
    ChapterAudioSerializer, 
    AudioTimestampSerializer
)


class ReciterViewSet(viewsets.ModelViewSet):
    queryset=Reciter.objects.all()
    serializer_class=ReciterSerializer

class ChapterAudioViewSet(viewsets.ModelViewSet):
    queryset=ChapterAudio.objects.all()
    serializer_class=ChapterAudioSerializer

class AudioTimestampsViewSet(viewsets.ModelViewSet):
    queryset=AudioTimestamp.objects.all()
    serializer_class=AudioTimestampSerializer        

