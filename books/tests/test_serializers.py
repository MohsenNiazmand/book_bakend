import pytest
from rest_framework.exceptions import ValidationError
from books.serializers import BookSerializer, ChapterSerializer, VerseSerializer
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from core.tests.factories import TenantFactory

class TestBookSerializer:
    """
    Unit tests for BookSerializer.
    Tests cover serialization, deserialization, and validation.
    """
    
    @pytest.mark.django_db
    def test_serialize_book(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that Book model is correctly converted to dictionary format.
        """
        book = BookFactory(title="Test Book", language="ar")
        serializer = BookSerializer(book)
        
        assert serializer.data['title'] == "Test Book"
        assert serializer.data['language'] == "ar"
        assert serializer.data['id'] == book.id
        assert 'tenant' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_book(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to Book model.
        """
        tenant = TenantFactory()
        data = {
            'title': 'New Book',
            'description': 'Description',
            'language': 'ar',
            'tenant': tenant.id
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid()
        
        book = serializer.save()
        assert book.title == 'New Book'
        assert book.tenant == tenant
    
    @pytest.mark.django_db
    def test_serializer_validation_required_fields(self):
        """
        Test serializer validation for required fields.
        Verifies that missing required fields raise validation errors.
        """
        data = {
            'description': 'Description only'
            # Missing title and tenant
        }
        serializer = BookSerializer(data=data)
        assert not serializer.is_valid()


class TestChapterSerializer:
    """
    Unit tests for ChapterSerializer.
    Tests cover serialization, deserialization, and validation.
    """
    
    @pytest.mark.django_db
    def test_serialize_chapter(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that Chapter model is correctly converted to dictionary format.
        """
        chapter = ChapterFactory(title="Test Chapter", number=1)
        serializer = ChapterSerializer(chapter)
        
        assert serializer.data['title'] == "Test Chapter"
        assert serializer.data['number'] == 1
        assert serializer.data['id'] == chapter.id
        assert 'book' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_chapter(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to Chapter model.
        """
        book = BookFactory()
        data = {
            'book': book.id,
            'title': 'New Chapter',
            'number': 1,
            'juz': 1
        }
        serializer = ChapterSerializer(data=data)
        assert serializer.is_valid()
        
        chapter = serializer.save()
        assert chapter.title == 'New Chapter'
        assert chapter.book == book


class TestVerseSerializer:
    """
    Unit tests for VerseSerializer.
    Tests cover serialization, deserialization, and validation.
    """
    
    @pytest.mark.django_db
    def test_serialize_verse(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that Verse model is correctly converted to dictionary format.
        """
        verse = VerseFactory(text="Test verse text", number=1)
        serializer = VerseSerializer(verse)
        
        assert serializer.data['text'] == "Test verse text"
        assert serializer.data['number'] == 1
        assert serializer.data['id'] == verse.id
        assert 'book' in serializer.data
        assert 'chapter' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_verse(self):
        """
        Test deserialization: dictionary -> model instance.
        Verifies that dictionary data is correctly converted to Verse model.
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        data = {
            'book': book.id,
            'chapter': chapter.id,
            'number': 1,
            'text': 'New verse text',
            'translation': 'Translation',
            'page_number': 1
        }
        serializer = VerseSerializer(data=data)
        assert serializer.is_valid()
        
        verse = serializer.save()
        assert verse.text == 'New verse text'
        assert verse.book == book
        assert verse.chapter == chapter

