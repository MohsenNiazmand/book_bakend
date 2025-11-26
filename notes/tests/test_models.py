import pytest
from django.db import IntegrityError
from notes.models import UserNote, Bookmark, PlayHistory
from notes.tests.factories import UserNoteFactory, BookmarkFactory, PlayHistoryFactory
from users.tests.factories import UserFactory
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from core.tests.factories import TenantFactory
from audio.tests.factories import ChapterAudioFactory

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



class TestBookmarkModel:
    """
    Unit tests for Bookmark model.
    Tests cover model creation, relationships, unique constraints, and tenant isolation.
    """
    
    @pytest.mark.django_db
    def test_create_bookmark(self):
        """
        Test successful creation of a Bookmark instance.
        Verifies that all required fields are properly set and saved to the database.
        """
        bookmark = BookmarkFactory()
        assert bookmark.id is not None
        assert bookmark.user is not None
        assert bookmark.book is not None
    
    @pytest.mark.django_db
    def test_bookmark_belongs_to_user_and_book(self):
        """
        Test that bookmark is correctly associated with user and book.
        Verifies the ForeignKey relationships.
        """
        user = UserFactory()
        book = BookFactory()
        bookmark = BookmarkFactory(user=user, book=book)
        
        assert bookmark.user == user
        assert bookmark.book == book
    
    @pytest.mark.django_db
    def test_bookmark_with_verse(self):
        """
        Test creating bookmark with verse reference.
        Verifies that bookmark can be associated with a specific verse.
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        bookmark = BookmarkFactory(book=book, verse=verse)
        
        assert bookmark.verse == verse
    
    @pytest.mark.django_db
    def test_bookmark_inherits_tenant_from_book(self):
        """
        Test that bookmark inherits tenant through book relationship.
        Verifies tenant isolation through book.
        """
        tenant = TenantFactory(domain="test")
        book = BookFactory(tenant=tenant)
        user = UserFactory(tenant=tenant)
        bookmark = BookmarkFactory(user=user, book=book)
        
        assert bookmark.book.tenant == tenant
        assert bookmark.user.tenant == tenant
    
    @pytest.mark.django_db
    def test_unique_bookmark_per_user_book_chapter_verse(self):
        """
        Test unique constraint: same user can bookmark same book+chapter+verse only once.
        Verifies the unique_together constraint ('user', 'book', 'chapter', 'verse').
        """
        user = UserFactory()
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        
        bookmark1 = BookmarkFactory(user=user, book=book, chapter=chapter, verse=verse)
        
        # Creating another bookmark with same combination should fail
        with pytest.raises(IntegrityError):
            BookmarkFactory(user=user, book=book, chapter=chapter, verse=verse)
    
    @pytest.mark.django_db
    def test_bookmark_optional_fields(self):
        """
        Test that optional fields (chapter, verse, page_number) can be None.
        Verifies that bookmarks can be created at book level.
        """
        bookmark = BookmarkFactory(chapter=None, verse=None, page_number=None)
        assert bookmark.chapter is None
        assert bookmark.verse is None
        assert bookmark.page_number is None   



class TestPlayHistoryModel:
    """
    Unit tests for PlayHistory model.
    Tests cover model creation, relationships, unique constraints, and tenant isolation.
    """
    
    @pytest.mark.django_db
    def test_create_play_history(self):
        """
        Test successful creation of a PlayHistory instance.
        Verifies that all required fields are properly set and saved to the database.
        """
        history = PlayHistoryFactory()
        assert history.id is not None
        assert history.user is not None
        assert history.chapter_audio is not None
        assert history.last_position is not None
    
    @pytest.mark.django_db
    def test_play_history_belongs_to_user_and_audio(self):
        """
        Test that play history is correctly associated with user and chapter_audio.
        Verifies the ForeignKey relationships.
        """
        user = UserFactory()
        audio = ChapterAudioFactory()
        history = PlayHistoryFactory(user=user, chapter_audio=audio)
        
        assert history.user == user
        assert history.chapter_audio == audio
    
    @pytest.mark.django_db
    def test_play_history_str(self):
        """
        Test the __str__ method of the PlayHistory model.
        Verifies that string representation includes user and chapter_audio.
        """
        user = UserFactory(username="testuser")
        audio = ChapterAudioFactory()
        history = PlayHistoryFactory(user=user, chapter_audio=audio)
        
        str_repr = str(history)
        assert "testuser" in str_repr
    
    @pytest.mark.django_db
    def test_play_history_inherits_tenant(self):
        """
        Test that play history inherits tenant through user and chapter_audio relationships.
        Verifies tenant isolation.
        """
        tenant = TenantFactory(domain="test")
        user = UserFactory(tenant=tenant)
        book = BookFactory(tenant=tenant)
        chapter = ChapterFactory(book=book)
        audio = ChapterAudioFactory(chapter=chapter)
        history = PlayHistoryFactory(user=user, chapter_audio=audio)
        
        assert history.user.tenant == tenant
        assert history.chapter_audio.chapter.book.tenant == tenant
    
    @pytest.mark.django_db
    def test_unique_play_history_per_user_audio(self):
        """
        Test unique constraint: same user can have play history for different audios.
        Actually, unique_together is ('user', 'chapter_audio'), so same audio for same user should update.
        But let's test that creating duplicate raises error (or updates - depends on implementation).
        """
        user = UserFactory()
        audio = ChapterAudioFactory()
        
        history1 = PlayHistoryFactory(user=user, chapter_audio=audio, last_position=10.0)
        
        # Creating another history with same user and audio should fail
        # (or update - but for now we test that it fails)
        with pytest.raises(IntegrityError):
            PlayHistoryFactory(user=user, chapter_audio=audio, last_position=20.0)
    
    @pytest.mark.django_db
    def test_play_history_last_position(self):
        """
        Test that last_position field stores the correct playback position.
        Verifies that position is saved and can be updated.
        """
        history = PlayHistoryFactory(last_position=50.5)
        assert history.last_position == 50.5
        
        history.last_position = 100.0
        history.save()
        assert history.last_position == 100.0             