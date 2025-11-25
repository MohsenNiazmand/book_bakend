from rest_framework import serializers
from .models import UserNote, Bookmark, PlayHistory


class UserNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserNote
        fields="__all__"
        read_only_fields=['user']
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookmark
        fields="__all__"
        read_only_fields=['user']
class PlayHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayHistory
        fields = '__all__'
        read_only_fields = ['user']
    


