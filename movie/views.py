from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from movie.serializer import UserDetailsSerializer, MovieRatingSerializer, RatingSerializer, FavGenreSerializer, \
    MovieDetailSerializer
from movie.models import Movie, UserDetails, Genre, Rating
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from movie.serializer import MovieSerializer


#views

class Register(generics.CreateAPIView):
    serializer_class = UserDetailsSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserDetailsSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Add_Movie(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MovieRatingSerializer

    def post(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        serializer1 = RatingSerializer(data=request.data)
        serializer1.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid() and serializer1.is_valid():
            movie = serializer.save(created_by=UserDetails.objects.get(user=request.user))
            ratings = serializer1.save(user=UserDetails.objects.get(user=request.user), movie=movie)
            return Response({
                "movie": MovieSerializer(movie, context=self.get_serializer_context()).data,
                "rating": RatingSerializer(ratings, context=self.get_serializer_context()).data,
                "message": "Successfully Add Movie",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Set_Favourite_Genre(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavGenreSerializer

    def patch(self, request, *args, **kwargs):
        model = UserDetails.objects.get(user=request.user)
        serializer = FavGenreSerializer(model, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Set Favorites Genre Successfully. ",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Get_Recomended_Movie(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        user_details = UserDetails.objects.get(user=request.user)
        model = Movie.objects.filter(genre=Genre.objects.get(id=user_details.fav_genre.id))
        return Response({
            "data": MovieSerializer(model, context=self.get_serializer_context(), many=True).data,
            "message": " Recomended movies ",
        })


class Set_UpVote_DownVote(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingSerializer

    def post(self, request, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = serializer.validated_data.get('movie')
        if Rating.objects.filter(movie=movie).filter(user=UserDetails.objects.get(user=request.user)).exists():
            model = Rating.objects.get(movie=movie, user=UserDetails.objects.get(user=request.user))
            serializer = RatingSerializer(model, data=request.data, partial=True)
            if serializer.is_valid():
                ratings = serializer.save(movie=movie, )
                return Response({
                    "rating": RatingSerializer(ratings, context=self.get_serializer_context()).data,
                    "message": "Successfully changed",
                })
        else:
            if serializer.is_valid():
                ratings = serializer.save(movie=movie, user=UserDetails.objects.get(user=request.user))
                return Response({
                    "rating": RatingSerializer(ratings, context=self.get_serializer_context()).data,
                    "message": "Successfully uploaded",
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieViewSet(generics.ListAPIView):
    queryset = Movie.objects.all().annotate(upvote_count=Count('rating__upvote', only=Q(ratings__upvote=True)),
                                            downvote_count=Count('rating__downvote',
                                                                 only=Q(ratings__downvote=True)))  # query result set
    serializer_class = MovieDetailSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('genre',)

    search_fields = ('title',)

    ordering_fields = ('upvote_count', 'downvote_count', 'genre',)
