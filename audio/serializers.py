from rest_framework import serializers
from .models import Reciter, ChapterAudio, AudioTimestamp


class ReciterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reciter
        fields = "__all__"

class ChapterAudioSerializer(serializers.ModelSerializer):
    reciter = ReciterSerializer(read_only=True)
    reciter_id = serializers.PrimaryKeyRelatedField(
        queryset=Reciter.objects.all(),
        source='reciter',
        write_only=True
    )

    class Meta:
        model = ChapterAudio
        fields = ['id', 'reciter', 'reciter_id', 'chapter_number', 'audio_file', 'duration']

class AudioTimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTimestamp
        fields = "__all__"

