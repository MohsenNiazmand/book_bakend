import factory
from notes.models import UserNote, Bookmark, PlayHistory
from users.tests.factories import UserFactory
from books.tests.factories import BookFactory, ChapterFactory, VerseFactory
from audio.tests.factories import ChapterAudioFactory

class UserNoteFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating UserNote instances in tests.
    Automatically creates user, book, and optionally chapter/verse.
    """
    class Meta:
        model = UserNote
    
    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory)
    chapter = None  # Optional
    verse = None  # Optional
    page_number = None  # Optional
    note_text = factory.Sequence(lambda n: f"Note text {n}")


class BookmarkFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating Bookmark instances in tests.
    Automatically creates user and book, and optionally chapter/verse.
    """
    class Meta:
        model = Bookmark
    
    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory)
    chapter = None  # Optional
    verse = None  # Optional
    page_number = None  # Optional


class PlayHistoryFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating PlayHistory instances in tests.
    Automatically creates user and chapter_audio.
    """
    class Meta:
        model = PlayHistory
    
    user = factory.SubFactory(UserFactory)
    chapter_audio = factory.SubFactory(ChapterAudioFactory)
    last_position = 0.0