from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('books.urls')),

    path('api/v1/audio/', include('audio.urls')),

    path('api/v1/notes/', include('notes.urls')),

    path("api/v1/auth/", include("accounts.urls")),

]
