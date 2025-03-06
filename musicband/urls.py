"""
URL configuration for musicband project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import review

from django.contrib import admin
from django.urls import path
from review.views import add_album, add_song,  add_comment
from review.views import update_album, update_song,  update_comment
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', review.views.index, name='home'),
    path('song-search/', review.views.song_search),
    path('add-album/', review.views.add_album, name='add_album'),
    path('add-song/', add_song, name='add_song'),
    path('add-comment/', add_comment, name='add_comment'),
path('update-album/<int:album_id>/', update_album, name='update_album'),
    path('update-song/<int:song_id>/', update_song, name='update_song'),
    path('update-comment/<int:comment_id>/', update_comment, name='update_comment'),

]
