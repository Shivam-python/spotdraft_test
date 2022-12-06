from django.urls import path
from .views import PlanetsList,MoviesList,FavouritesApi

urlpatterns = [
    path("movies_list/",MoviesList.as_view(),name='movies'),
    path("planets_list/",PlanetsList.as_view(),name='planets'),
    path("favourites/",FavouritesApi.as_view(),name='favourites'),
    path("favourites/<str:pk>",FavouritesApi.as_view(),name='favourite-details')
]