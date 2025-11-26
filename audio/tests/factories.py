import factory
from audio.models import Reciter, ChapterAudio, AudioTimestamp
from core.tests.factories import TenantFactory
from books.tests.factories import ChapterFactory, VerseFactory

class ReciterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reciter

    tenant = factory.SubFactory(TenantFactory)
    name = factory.Sequence(lambda n: f"Reciter {n}")
    language = "ar"
    bio = factory.Faker('text')

class ChapterAudioFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating ChapterAudio instances in tests.
    Automatically creates chapter and reciter, and sets external_url by default.
    """
    class Meta:
        model = ChapterAudio
    
    chapter = factory.SubFactory(ChapterFactory)
    reciter = factory.SubFactory(ReciterFactory)
    external_url = factory.Sequence(lambda n: f"https://example.com/audio{n}.mp3")
    file = None  # Optional - can be set manually for file upload tests
    duration_seconds = 300

class AudioTimestampFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating AudioTimestamp instances in tests.
    Automatically creates chapter_audio and verse, ensuring they belong to same chapter.
    """
    class Meta:
        model = AudioTimestamp
    
    chapter_audio = factory.SubFactory(ChapterAudioFactory)
    verse = factory.SubFactory(
        VerseFactory,
        chapter=factory.SelfAttribute('..chapter_audio.chapter'),
        book=factory.SelfAttribute('..chapter_audio.chapter.book')
    )
    start_time = 0.0
    end_time = 10.0