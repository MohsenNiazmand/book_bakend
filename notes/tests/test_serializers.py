import pytest
from rest_framework.exceptions import ValidationError
from notes.serializers import UserNoteSerializer, BookmarkSerializer, PlayHistorySerializer
from notes.tests.factories import UserNoteFactory, BookmarkFactory, PlayHistoryFactory
from users.tests.factories import UserFactory
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from core.tests.factories import TenantFactory

class TestUserNoteSerializer:
    """
    Unit tests for UserNoteSerializer.
    Tests cover serialization, deserialization, and read-only user field.
    """
    
    @pytest.mark.django_db
    def test_serialize_user_note(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that UserNote model is correctly converted to dictionary format.
        """
        note = UserNoteFactory(note_text="Test note")
        serializer = UserNoteSerializer(note)
        
        assert serializer.data['note_text'] == "Test note"
        assert serializer.data['id'] == note.id
        assert 'user' in serializer.data
        assert 'book' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_user_note(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to UserNote model.
        Note: user field is read-only and should be set separately.
        """
        user = UserFactory()
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        
        data = {
            'book': book.id,
            'chapter': chapter.id,
            'verse': verse.id,
            'note_text': 'New note text',
            'page_number': 1
        }
        serializer = UserNoteSerializer(data=data)
        assert serializer.is_valid()
        
        # Note: user should be set in view's perform_create, but for test we set it manually
        note = serializer.save(user=user)
        assert note.note_text == 'New note text'
        assert note.book == book
        assert note.user == user
    
    @pytest.mark.django_db
    def test_serializer_user_read_only(self):
        """
        Test that user field is read-only in serializer.
        Verifies that user cannot be set through serializer data, but can be set manually.
        """
        user = UserFactory()
        book = BookFactory()
        
        data = {
            'user': user.id,  # Should be ignored (read-only)
            'book': book.id,
            'note_text': 'Test note'
        }
        serializer = UserNoteSerializer(data=data)
        assert serializer.is_valid()
        
        # User from data is ignored, must be set manually
        note = serializer.save(user=user)
        assert note.user == user  # User was set manually, not from data
        assert note.book == book
        assert note.note_text == 'Test note'


class TestBookmarkSerializer:
    """
    Unit tests for BookmarkSerializer.
    Tests cover serialization, deserialization, and read-only user field.
    """
    
    @pytest.mark.django_db
    def test_serialize_bookmark(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that Bookmark model is correctly converted to dictionary format.
        """
        bookmark = BookmarkFactory()
        serializer = BookmarkSerializer(bookmark)
        
        assert serializer.data['id'] == bookmark.id
        assert 'user' in serializer.data
        assert 'book' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_bookmark(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to Bookmark model.
        Note: user field is read-only and should be set separately.
        """
        user = UserFactory()
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        
        data = {
            'book': book.id,
            'chapter': chapter.id,
            'verse': verse.id,
            'page_number': 1
        }
        serializer = BookmarkSerializer(data=data)
        assert serializer.is_valid()
        
        # User should be set in view's perform_create, but for test we set it manually
        bookmark = serializer.save(user=user)
        assert bookmark.book == book
        assert bookmark.chapter == chapter
        assert bookmark.user == user


class TestPlayHistorySerializer:
    """
    Unit tests for PlayHistorySerializer.
    Tests cover serialization, deserialization, and read-only user field.
    """
    
    @pytest.mark.django_db
    def test_serialize_play_history(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that PlayHistory model is correctly converted to dictionary format.
        """
        history = PlayHistoryFactory(last_position=50.5)
        serializer = PlayHistorySerializer(history)
        
        assert serializer.data['last_position'] == 50.5
        assert serializer.data['id'] == history.id
        assert 'user' in serializer.data
        assert 'chapter_audio' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_play_history(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to PlayHistory model.
        Note: user field is read-only and should be set separately.
        """
        from audio.tests.factories import ChapterAudioFactory
        from books.tests.factories import ChapterFactory
        
        user = UserFactory()
        chapter = ChapterFactory()
        audio = ChapterAudioFactory(chapter=chapter)
        data = {
            'chapter_audio': audio.id,
            'last_position': 100.0
        }
        serializer = PlayHistorySerializer(data=data)
        assert serializer.is_valid()
        
        # User should be set in view's perform_create, but for test we set it manually
        history = serializer.save(user=user)
        assert history.last_position == 100.0
        assert history.chapter_audio == audio
        assert history.user == user

