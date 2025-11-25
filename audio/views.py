from rest_framework import viewsets
from core.middleware import get_current_tenant
from .models import Reciter, ChapterAudio, AudioTimestamp
from .serializers import (
    ReciterSerializer, 
    ChapterAudioSerializer, 
    AudioTimestampSerializer
)


class ReciterViewSet(viewsets.ModelViewSet):
    serializer_class = ReciterSerializer
    
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant:
            return Reciter.objects.filter(tenant=tenant)
        return Reciter.objects.none()
    
    def perform_create(self, serializer):
        tenant = get_current_tenant()
        if tenant:
            serializer.save(tenant=tenant)

class ChapterAudioViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterAudioSerializer
    
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant:
            # Filter by tenant through chapter->book relationship
            return ChapterAudio.objects.filter(chapter__book__tenant=tenant)
        return ChapterAudio.objects.none()
    
    def perform_create(self, serializer):
        tenant = get_current_tenant()
        if tenant:
            chapter = serializer.validated_data.get('chapter')
            if chapter and chapter.book.tenant == tenant:
                serializer.save()

class AudioTimestampsViewSet(viewsets.ModelViewSet):
    serializer_class = AudioTimestampSerializer
    
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant:
            # Filter by tenant through chapter_audio->chapter->book relationship
            return AudioTimestamp.objects.filter(chapter_audio__chapter__book__tenant=tenant)
        return AudioTimestamp.objects.none()        

