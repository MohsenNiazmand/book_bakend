from rest_framework.routers import DefaultRouter
from .views import ReciterViewSet,ChapterAudioViewSet,AudioTimestampsViewSet


router=DefaultRouter()
router.register('reciters',ReciterViewSet)
router.register('chapter-audios',ChapterAudioViewSet)
router.register('timestamps',AudioTimestampsViewSet)

urlpatterns = router.urls
