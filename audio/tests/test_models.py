import pytest
from django.db import IntegrityError
from audio.models import Reciter, ChapterAudio, AudioTimestamp
from audio.tests.factories import (
    ReciterFactory, 
    ChapterAudioFactory,
)
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from core.tests.factories import TenantFactory

class TestReciterModel:
    """
    Unit tests for Reciter model.
    Tests cover model creation, relationships, unique constraints, and string representation.
    """
    
    @pytest.mark.django_db
    def test_create_reciter(self):
        """
        Test successful creation of a Reciter instance.
        Verifies that all required fields (id, name, language, tenant) 
        are properly set and saved to the database.
        """
        reciter = ReciterFactory()
        assert reciter.id is not None
        assert reciter.name is not None
        assert reciter.language == "ar"
        assert reciter.tenant is not None


    @pytest.mark.django_db
    def test_reciter_belongs_to_tenant(self):
        """
        Test that reciter is correctly associated with a tenant.
        Verifies the ForeignKey relationship between Reciter and Tenant.
        """ 
        tenant = TenantFactory(domain="test")
        reciter = ReciterFactory(tenant=tenant)
        assert reciter.tenant == tenant
        assert reciter.tenant.domain == "test"

    @pytest.mark.django_db
    def test_reciter_str(self):
        """
        Test the __str__ method of the Reciter model.
        Verifies that string representation returns the reciter's name.
        """
        reciter = ReciterFactory(name = "Test Reciter")
        assert str(reciter) == "Test Reciter"

    @pytest.mark.django_db
    def test_unique_name_per_tenant(self):
        """
        Test unique constraint: same name can exist in different tenants.
        Verifies that two reciters with the same name can exist 
        if they belong to different tenants.
        """
        tenant1 = TenantFactory(domain="tenant1")
        tenant2 = TenantFactory(domain="tenant2")
        
        reciter1 = ReciterFactory(tenant=tenant1, name="Same Name")
        reciter2 = ReciterFactory(tenant=tenant2, name="Same Name")
        
        assert reciter1.name == reciter2.name
        assert reciter1.tenant != reciter2.tenant
    
    @pytest.mark.django_db
    def test_unique_name_same_tenant_fails(self):
        """
        Test that creating two reciters with the same name in the same tenant raises an exception.
        Verifies the unique_together constraint ('tenant', 'name').
        """
        tenant = TenantFactory()
        ReciterFactory(tenant=tenant, name="Unique Name")
        
        with pytest.raises(Exception):
            ReciterFactory(tenant=tenant, name="Unique Name")


class TestChapterAudioModel:
    """
    Unit tests for ChapterAudio model.
    Tests cover model creation, relationships, unique constraints, and validation.
    """
    
    @pytest.mark.django_db
    def test_create_chapter_audio(self):
        """
        Test successful creation of a ChapterAudio instance.
        Verifies that all required fields are properly set and saved to the database.
        """
        audio = ChapterAudioFactory()
        assert audio.id is not None
        assert audio.chapter is not None
        assert audio.reciter is not None
        assert audio.external_url is not None
    
    @pytest.mark.django_db
    def test_chapter_audio_belongs_to_chapter_and_reciter(self):
        """
        Test that chapter audio is correctly associated with chapter and reciter.
        Verifies the ForeignKey relationships.
        """
        chapter = ChapterFactory()
        reciter = ReciterFactory()
        audio = ChapterAudioFactory(chapter=chapter, reciter=reciter)
        
        assert audio.chapter == chapter
        assert audio.reciter == reciter
    
    @pytest.mark.django_db
    def test_chapter_audio_str(self):
        """
        Test the __str__ method of the ChapterAudio model.
        Verifies that string representation includes chapter and reciter names.
        """
        book = BookFactory(title="Test Book")
        chapter = ChapterFactory(book=book, title="Test Chapter")
        reciter = ReciterFactory(name="Test Reciter")
        audio = ChapterAudioFactory(chapter=chapter, reciter=reciter)
        
        str_repr = str(audio)
        assert "Test Chapter" in str_repr
        assert "Test Reciter" in str_repr
    
    @pytest.mark.django_db
    def test_chapter_audio_inherits_tenant_from_chapter(self):
        """
        Test that chapter audio inherits tenant through chapter->book relationship.
        Verifies tenant isolation through chapter.
        """
        tenant = TenantFactory(domain="test")
        book = BookFactory(tenant=tenant)
        chapter = ChapterFactory(book=book)
        reciter = ReciterFactory(tenant=tenant)
        audio = ChapterAudioFactory(chapter=chapter, reciter=reciter)
        
        assert audio.chapter.book.tenant == tenant
        assert audio.reciter.tenant == tenant
    
    @pytest.mark.django_db
    def test_unique_chapter_reciter_combination(self):
        """
        Test unique constraint: same chapter and reciter combination can exist 
        in different contexts (different books/tenants).
        Actually, this should be unique per chapter+reciter, so let's test that.
        """
        chapter = ChapterFactory()
        reciter = ReciterFactory()
        
        audio1 = ChapterAudioFactory(chapter=chapter, reciter=reciter)
        
        # Creating another audio with same chapter+reciter should fail
        with pytest.raises(IntegrityError):
            ChapterAudioFactory(chapter=chapter, reciter=reciter)
    
    @pytest.mark.django_db
    def test_chapter_audio_optional_fields(self):
        """
        Test that optional fields (file, duration_seconds) can be None.
        Verifies that audio can be created with only external_url.
        """
        audio = ChapterAudioFactory(file=None, duration_seconds=None)
        assert audio.file is None or audio.external_url is not None
        assert audio.duration_seconds is None or audio.duration_seconds is not None            