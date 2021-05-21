from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('boards/', include('boards.urls')),
    path('movies/', include('movies.urls')),
    path('recommends/', include('recommends.urls')),
]
