"""movie_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from movie.views import Register, Add_Movie, Set_Favourite_Genre, Get_Recomended_Movie, Set_UpVote_DownVote, \
    MovieViewSet

urlpatterns = [
    path('movie-view-set', MovieViewSet.as_view()),
    path('register', Register.as_view(), name='token_obtain_pair'),

    path('add-Movie', Add_Movie.as_view()),
    path('set-favourite-genre', Set_Favourite_Genre.as_view()),
    path('get_recomended_movie', Get_Recomended_Movie.as_view()),
    path('set_UpVote-DownVote', Set_UpVote_DownVote.as_view()),

]
