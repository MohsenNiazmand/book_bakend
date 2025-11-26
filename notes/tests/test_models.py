import pytest
from django.db import IntegrityError
from notes.models import UserNote, Bookmark, PlayHistory
from notes.tests.factories import UserNoteFactory, BookmarkFactory, PlayHistoryFactory
from users.tests.factories import UserFactory
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from core.tests.factories import TenantFactory

class TestUserNoteModel:
    """
    Unit tests for UserNote model.
    Tests cover model creation, relationships, unique constraints, and tenant isolation.
    """
    
    @pytest.mark.django_db
    def test_create_user_note(self):
        """
        Test successful creation of a UserNote instance.
        Verifies that all required fields are properly set and saved to the database.
        """
        note = UserNoteFactory()
        assert note.id is not None
        assert note.user is not None
        assert note.book is not None
        assert note.note_text is not None
    
    @pytest.mark.django_db
    def test_user_note_belongs_to_user_and_book(self):
        """
        Test that note is correctly associated with user and book.
        Verifies the ForeignKey relationships.
        """
        user = UserFactory()
        book = BookFactory()
        note = UserNoteFactory(user=user, book=book)
        
        assert note.user == user
        assert note.book == book
    
    @pytest.mark.django_db
    def test_user_note_with_verse(self):
        """
        Test creating note with verse reference.
        Verifies that note can be associated with a specific verse.
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        note = UserNoteFactory(book=book, verse=verse)
        
        assert note.verse == verse
        assert note.verse.chapter == chapter
    
    @pytest.mark.django_db
    def test_user_note_inherits_tenant_from_book(self):
        """
        Test that note inherits tenant through book relationship.
        Verifies tenant isolation through book.
        """
        tenant = TenantFactory(domain="test")
        book = BookFactory(tenant=tenant)
        user = UserFactory(tenant=tenant)
        note = UserNoteFactory(user=user, book=book)
        
        assert note.book.tenant == tenant
        assert note.user.tenant == tenant
    
    @pytest.mark.django_db
    def test_unique_note_per_user_verse(self):
        """
        Test unique constraint: same user can have notes for different verses.
        Actually, unique_together is ('user', 'verse'), so same verse for same user should fail.
        """
        user = UserFactory()
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        
        note1 = UserNoteFactory(user=user, book=book, verse=verse)
        
        # Creating another note with same user and verse should fail
        with pytest.raises(IntegrityError):
            UserNoteFactory(user=user, book=book, verse=verse)
    
    @pytest.mark.django_db
    def test_user_note_optional_fields(self):
        """
        Test that optional fields (chapter, verse, page_number) can be None.
        Verifies that notes can be created at book level without chapter/verse.
        """
        note = UserNoteFactory(chapter=None, verse=None, page_number=None)
        assert note.chapter is None
        assert note.verse is None
        assert note.page_number is None