from django.urls import path
from  .views import (FavoritListView,CreateFavoritView,UpdateFavoriteView,DeleteFavoriteView)

urlpatterns = [
    
    path("favorit/list/",FavoritListView.as_view(),name="favorit-list"),
    path("favorit/create/<slug:slug>/",CreateFavoritView.as_view(),name="favorit-create"),
    path("favorit/update/<slug:slug>/",UpdateFavoriteView.as_view(),name="favorit-update"),
    path("favorite/delete/<slug:slug>/",DeleteFavoriteView.as_view(),name="favorite-delete"),
]
