import pytest
from books.models import Book
from django.db import IntegrityError
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from core.tests.factories import TenantFactory

class TestBookModel:
    """
    Unit tests for Book model.
    Tests cover model creation, tenant association, unique constraints, and relationships.
    """
    
    @pytest.mark.django_db
    def test_create_book(self):
        """
        Test successful creation of a Book instance.
        Verifies that all required fields are properly set and saved to the database.
        """
        book = BookFactory()
        assert book.id is not None
        assert book.title is not None
        assert book.tenant is not None
        assert book.language == "ar"
    
    @pytest.mark.django_db
    def test_book_belongs_to_tenant(self):
        """
        Test that book is correctly associated with a tenant.
        Verifies the ForeignKey relationship between Book and Tenant.
        """
        tenant = TenantFactory(domain="test")
        book = BookFactory(tenant=tenant)
        assert book.tenant == tenant
        assert book.tenant.domain == "test"
    
    @pytest.mark.django_db
    def test_book_str(self):
        """
        Test the __str__ method of the Book model.
        Verifies that string representation returns the book's title.
        """
        book = BookFactory(title="Test Book")
        assert str(book) == "Test Book"
    
    @pytest.mark.django_db
    def test_unique_title_per_tenant(self):
        """
        Test unique constraint: same title can exist in different tenants.
        Verifies that two books with the same title can exist 
        if they belong to different tenants.
        """
        tenant1 = TenantFactory(domain="tenant1")
        tenant2 = TenantFactory(domain="tenant2")
        
        book1 = BookFactory(tenant=tenant1, title="Same Title")
        book2 = BookFactory(tenant=tenant2, title="Same Title")
        
        assert book1.title == book2.title
        assert book1.tenant != book2.tenant
    
    @pytest.mark.django_db
    def test_unique_title_same_tenant_fails(self):
        """
        Test that creating two books with the same title in the same tenant raises an exception.
        Verifies the unique_together constraint ('tenant', 'title').
        """
        tenant = TenantFactory()
        BookFactory(tenant=tenant, title="Unique Title")
        
        with pytest.raises(Exception):
            BookFactory(tenant=tenant, title="Unique Title")


class TestChapterModel:
    """
    Unit tests for Chapter model.
    Tests cover model creation, book relationship, and string representation.
    """
    
    @pytest.mark.django_db
    def test_create_chapter(self):
        """
        Test successful creation of a Chapter instance.
        Verifies that all required fields (id, title, number, book) 
        are properly set and saved to the database.
        """
        chapter = ChapterFactory()
        assert chapter.id is not None
        assert chapter.title is not None
        assert chapter.number is not None
        assert chapter.book is not None
    
    @pytest.mark.django_db
    def test_chapter_belongs_to_book(self):
        """
        Test that chapter is correctly associated with a book.
        Verifies the ForeignKey relationship between Chapter and Book.
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        assert chapter.book == book
        assert chapter.book.tenant is not None
    
    @pytest.mark.django_db
    def test_chapter_str(self):
        """
        Test the __str__ method of the Chapter model.
        Verifies that string representation returns the expected format.
        """
        book = BookFactory(title="Test Book")
        chapter = ChapterFactory(book=book, title="Test Chapter")
        # Format: "Book Title - Chapter Title"
        assert "Test Book" in str(chapter)
        assert "Test Chapter" in str(chapter)
    
    @pytest.mark.django_db
    def test_chapter_inherits_tenant_from_book(self):
        """
        Test that chapter inherits tenant through book relationship.
        Verifies tenant isolation through book.
        """
        tenant = TenantFactory(domain="test")
        book = BookFactory(tenant=tenant)
        chapter = ChapterFactory(book=book)
        
        assert chapter.book.tenant == tenant
        assert chapter.book.tenant.domain == "test"
    
    @pytest.mark.django_db
    def test_chapter_juz_optional(self):
        """
        Test that juz field is optional and can be None.
        Verifies that chapters can be created without juz value.
        """
        chapter = ChapterFactory(juz=None)
        assert chapter.juz is None
        
        chapter_with_juz = ChapterFactory(juz=1)
        assert chapter_with_juz.juz == 1


class TestVerseModel:
    """
    Unit tests for Verse model.
    Tests cover model creation, relationships, unique constraints, and tenant isolation.
    """
    
    @pytest.mark.django_db
    def test_create_verse(self):
        """
        Test successful creation of a Verse instance.
        Verifies that all required fields (id, number, text, book, chapter) 
        are properly set and saved to the database.
        """
        verse = VerseFactory()
        assert verse.id is not None
        assert verse.number is not None
        assert verse.text is not None
        assert verse.book is not None
        assert verse.chapter is not None
    
    @pytest.mark.django_db
    def test_verse_belongs_to_book_and_chapter(self):
        """
        Test that verse is correctly associated with both book and chapter.
        Verifies the ForeignKey relationships.
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        
        assert verse.book == book
        assert verse.chapter == chapter
        assert verse.chapter.book == book
    
    @pytest.mark.django_db
    def test_verse_str(self):
        """
        Test the __str__ method of the Verse model.
        Verifies that string representation includes chapter title, number, and page.
        """
        book = BookFactory(title="Test Book")
        chapter = ChapterFactory(book=book, title="Test Chapter")
        verse = VerseFactory(book=book, chapter=chapter, number=5, page_number=10)
        
        str_repr = str(verse)
        assert "Test Chapter" in str_repr
        assert "5" in str_repr
        assert "10" in str_repr
    
    @pytest.mark.django_db
    def test_verse_inherits_tenant_from_book(self):
        """
        Test that verse inherits tenant through book relationship.
        Verifies tenant isolation through book.
        """
        tenant = TenantFactory(domain="test")
        book = BookFactory(tenant=tenant)
        chapter = ChapterFactory(book=book)
        verse = VerseFactory(book=book, chapter=chapter)
        
        assert verse.book.tenant == tenant
        assert verse.chapter.book.tenant == tenant
    
    @pytest.mark.django_db
    def test_unique_verse_number_per_chapter(self):
        """
        Test unique constraint: same verse number can exist in different chapters.
        Verifies that two verses with the same number can exist 
        if they belong to different chapters.
        """
        book = BookFactory()
        chapter1 = ChapterFactory(book=book, number=1)
        chapter2 = ChapterFactory(book=book, number=2)
        
        verse1 = VerseFactory(book=book, chapter=chapter1, number=1)
        verse2 = VerseFactory(book=book, chapter=chapter2, number=1)
        
        assert verse1.number == verse2.number
        assert verse1.chapter != verse2.chapter
    
    @pytest.mark.django_db
    def test_unique_verse_number_same_chapter_fails(self):
        """
        Test that creating two verses with the same number in the same chapter raises an exception.
        Verifies the unique_together constraint ('chapter', 'number').
        """
        book = BookFactory()
        chapter = ChapterFactory(book=book)
        
        VerseFactory(book=book, chapter=chapter, number=1)
        
        with pytest.raises(IntegrityError):
            VerseFactory(book=book, chapter=chapter, number=1)
    
    @pytest.mark.django_db
    def test_verse_optional_fields(self):
        """
        Test that optional fields (translation, page_number) can be None.
        Verifies that verses can be created without these fields.
        """
        verse = VerseFactory(translation="", page_number=None)
        assert verse.translation == ""
        assert verse.page_number is None
        
        verse_with_fields = VerseFactory(translation="Translation", page_number=10)
        assert verse_with_fields.translation == "Translation"
        assert verse_with_fields.page_number == 10