from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UserNote, Bookmark, PlayHistory
from .serializers import (
    UserNoteSerializer,
    BookmarkSerializer,
    PlayHistorySerializer
)


class UserNoteViewSet(viewsets.ModelViewSet):
    serializer_class=UserNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserNote.objects.filter(user=self.request.user) 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class=BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user) 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class PlayHistoryViewSet(viewsets.ModelViewSet):
    serializer_class=PlayHistorySerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return PlayHistory.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
    


