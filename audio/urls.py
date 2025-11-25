from rest_framework.routers import DefaultRouter
from .views import ReciterViewSet,ChapterAudioViewSet,AudioTimestampsViewSet


router=DefaultRouter()
router.register('reciters',ReciterViewSet, basename='reciter')
router.register('chapter-audios',ChapterAudioViewSet, basename='chapter-audio')
router.register('timestamps',AudioTimestampsViewSet, basename='audio-timestamp')

urlpatterns = router.urls
