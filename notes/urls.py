from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserNoteViewSet, BookmarkViewSet, PlayHistoryViewSet


router=DefaultRouter()
router.register(r'notes',UserNoteViewSet, basename='notes')
router.register(r'bookmarks',BookmarkViewSet,basename='bookmarks')
router.register(r'history',PlayHistoryViewSet)

urlpatterns = [
    path=('',include(router.urls)),
]
