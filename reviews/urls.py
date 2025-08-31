from django.urls import path
from .views import (RatingListView,CreateRatingView,UpdateRatingView,DeleteRatingView)

urlpatterns = [

    path("list/",RatingListView.as_view(),name="rating-list"),
    path("create/<slug:slug>/",CreateRatingView.as_view(),name='rating-create'),
    path("update/<slug:slug>/",UpdateRatingView.as_view(),name="rating-update"),
    path("delete/<slug:slug>/",DeleteRatingView.as_view(),name="rating-delete"),
    
   
]
