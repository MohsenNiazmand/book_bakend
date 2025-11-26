import factory
from audio.models import Reciter, ChapterAudio
from core.tests.factories import TenantFactory
from books.tests.factories import ChapterFactory

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