from rest_framework import serializers
from django.contrib.auth.models import User
from movie.models import Movie, UserDetails, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = UserDetails
        fields = ['user', 'fav_genre', ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_detail = UserSerializer(data=user_data)
        if user_detail.is_valid():
            m = user_detail.save()
        a = UserDetails.objects.create(user=m, **validated_data)
        return a


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('created_by',)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ("user",)


class MovieRatingSerializer(serializers.Serializer):
    movie = MovieSerializer(many=True)
    rating = RatingSerializer(many=True)


class FavGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ["fav_genre", ]


class MovieDetailSerializer(serializers.ModelSerializer):
    genre = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        model = Movie
        exclude = ("created_by",)

    upvote_count = serializers.IntegerField()
    downvote_count = serializers.IntegerField()
