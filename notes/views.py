from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.middleware import get_current_tenant

from .models import UserNote, Bookmark, PlayHistory
from .serializers import (
    UserNoteSerializer,
    BookmarkSerializer,
    PlayHistorySerializer
)


class UserNoteViewSet(viewsets.ModelViewSet):
    serializer_class = UserNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tenant = get_current_tenant()
        queryset = UserNote.objects.filter(user=self.request.user)
        if tenant:
            # Filter by tenant through book relationship
            queryset = queryset.filter(book__tenant=tenant)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tenant = get_current_tenant()
        queryset = Bookmark.objects.filter(user=self.request.user)
        if tenant:
            # Filter by tenant through book relationship
            queryset = queryset.filter(book__tenant=tenant)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class PlayHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = PlayHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tenant = get_current_tenant()
        queryset = PlayHistory.objects.filter(user=self.request.user)
        if tenant:
            # Filter by tenant through chapter_audio->chapter->book relationship
            queryset = queryset.filter(chapter_audio__chapter__book__tenant=tenant)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
    


