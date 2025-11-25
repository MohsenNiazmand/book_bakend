from rest_framework import serializers
from .models import Reciter, ChapterAudio, AudioTimestamp
from books.models import Chapter


class ReciterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reciter
        fields = "__all__"


class ChapterAudioSerializer(serializers.ModelSerializer):
    # nested read-only reciter representation
    reciter = ReciterSerializer(read_only=True)
    # write-only field to set reciter by id
    reciter_id = serializers.PrimaryKeyRelatedField(
        queryset=Reciter.objects.all(),
        source='reciter',
        write_only=True,
        required=False,
    )
    # write-only field to set chapter by id
    chapter_id = serializers.PrimaryKeyRelatedField(
        queryset=Chapter.objects.all(),
        source='chapter',
        write_only=True,
        required=True,
    )

    class Meta:
        model = ChapterAudio
        # use actual model field names; include external_url and created_at for convenience
        fields = [
            'id', 'reciter', 'reciter_id', 'chapter', 'chapter_id',
            'external_url', 'file', 'duration_seconds', 'created_at'
        ]
        read_only_fields = ['id', 'reciter', 'chapter', 'created_at']


class AudioTimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTimestamp
        fields = "__all__"

