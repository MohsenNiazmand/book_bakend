import pytest
from rest_framework.exceptions import ValidationError
from audio.serializers import (
    ReciterSerializer, 
    ChapterAudioSerializer, 
    AudioTimestampSerializer
)
from audio.tests.factories import ReciterFactory, ChapterAudioFactory, AudioTimestampFactory
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from core.tests.factories import TenantFactory

class TestReciterSerializer:
    """
    Unit tests for ReciterSerializer.
    Tests cover serialization, deserialization, and validation.
    """
    
    @pytest.mark.django_db
    def test_serialize_reciter(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that Reciter model is correctly converted to dictionary format.
        """
        reciter = ReciterFactory(name="Test Reciter", language="ar")
        serializer = ReciterSerializer(reciter)
        
        assert serializer.data['name'] == "Test Reciter"
        assert serializer.data['language'] == "ar"
        assert serializer.data['id'] == reciter.id
        assert 'tenant' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_reciter(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to Reciter model.
        """
        tenant = TenantFactory()
        data = {
            'name': 'New Reciter',
            'language': 'ar',
            'bio': 'Test bio',
            'tenant': tenant.id
        }
        serializer = ReciterSerializer(data=data)
        assert serializer.is_valid()
        
        reciter = serializer.save()
        assert reciter.name == 'New Reciter'
        assert reciter.tenant == tenant


class TestChapterAudioSerializer:
    """
    Unit tests for ChapterAudioSerializer.
    Tests cover nested serialization, write-only fields, and validation.
    """
    
    @pytest.mark.django_db
    def test_serialize_chapter_audio(self):
        """
        Test serialization: includes nested reciter data.
        Verifies that reciter is serialized as nested object (read-only).
        """
        audio = ChapterAudioFactory()
        serializer = ChapterAudioSerializer(audio)
        
        assert 'reciter' in serializer.data
        assert serializer.data['reciter']['name'] == audio.reciter.name
        assert 'reciter_id' not in serializer.data  # write-only, not in output
        assert 'chapter_id' not in serializer.data  # write-only, not in output
    
    @pytest.mark.django_db
    def test_deserialize_chapter_audio_with_ids(self):
        """
        Test deserialization: uses write-only fields (reciter_id, chapter_id).
        Verifies that reciter_id and chapter_id are used for creation.
        """
        chapter = ChapterFactory()
        reciter = ReciterFactory()
        
        data = {
            'chapter_id': chapter.id,
            'reciter_id': reciter.id,
            'external_url': 'https://example.com/audio.mp3',
            'duration_seconds': 300
        }
        serializer = ChapterAudioSerializer(data=data)
        assert serializer.is_valid()
        
        audio = serializer.save()
        assert audio.chapter == chapter
        assert audio.reciter == reciter
    
    @pytest.mark.django_db
    def test_serializer_read_only_fields(self):
        """
        Test that read-only fields (id, reciter, chapter, created_at) are not writable.
        Verifies read_only_fields configuration.
        """
        audio = ChapterAudioFactory()
        data = {
            'id': 999,  # Should be ignored
            'chapter_id': audio.chapter.id,
            'reciter_id': audio.reciter.id,
            'external_url': 'https://example.com/new.mp3'
        }
        serializer = ChapterAudioSerializer(audio, data=data, partial=True)
        assert serializer.is_valid()
        
        updated_audio = serializer.save()
        assert updated_audio.id == audio.id  # ID should not change


class TestAudioTimestampSerializer:
    """
    Unit tests for AudioTimestampSerializer.
    Tests cover serialization, deserialization, and validation.
    """
    
    @pytest.mark.django_db
    def test_serialize_audio_timestamp(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that AudioTimestamp model is correctly converted to dictionary format.
        """
        timestamp = AudioTimestampFactory(start_time=10.0, end_time=20.0)
        serializer = AudioTimestampSerializer(timestamp)
        
        assert serializer.data['start_time'] == 10.0
        assert serializer.data['end_time'] == 20.0
        assert serializer.data['id'] == timestamp.id
        assert 'chapter_audio' in serializer.data
        assert 'verse' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_audio_timestamp(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to AudioTimestamp model.
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(chapter=chapter, book=book)
        audio = ChapterAudioFactory(chapter=chapter)
        
        data = {
            'chapter_audio': audio.id,
            'verse': verse.id,
            'start_time': 5.0,
            'end_time': 15.0
        }
        serializer = AudioTimestampSerializer(data=data)
        assert serializer.is_valid()
        
        timestamp = serializer.save()
        assert timestamp.start_time == 5.0
        assert timestamp.end_time == 15.0
        assert timestamp.chapter_audio == audio
        assert timestamp.verse == verse
    
    @pytest.mark.django_db
    def test_audio_timestamp_end_time_optional(self):
        """
        Test that end_time field is optional in serializer.
        Verifies that timestamps can be created without end_time.
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(chapter=chapter, book=book)
        audio = ChapterAudioFactory(chapter=chapter)
        
        data = {
            'chapter_audio': audio.id,
            'verse': verse.id,
            'start_time': 10.0
            # end_time is optional
        }
        serializer = AudioTimestampSerializer(data=data)
        assert serializer.is_valid()
        
        timestamp = serializer.save()
        assert timestamp.start_time == 10.0
        assert timestamp.end_time is None

