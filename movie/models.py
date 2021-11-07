# Create your models here.

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def id(self):
        return self.id


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    fav_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Movie(models.Model):
    title = models.CharField(max_length=140)
    synopsis = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    director = models.CharField(max_length=140)
    created_by = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    release_date = models.DateField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    upvote = models.BooleanField(blank=True, null=True)
    downvote = models.BooleanField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.movie.title
