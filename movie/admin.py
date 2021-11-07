# Register your models here.


from django.contrib import admin
from movie.models import Movie

from movie.models import Rating, Genre, UserDetails


class MovieAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, MovieAdmin)


class RatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rating, RatingAdmin)


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserDetails, UserDetailsAdmin)
