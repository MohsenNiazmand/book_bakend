from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ChapterViewSet, VerseViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'verses', VerseViewSet, basename='verse')

urlpatterns = router.urls
