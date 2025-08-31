from  django.urls import path
from .views import (
    CategoriesListView,
    CategoriesDetailsView,
    CreateCategoryView,
    UpdateCategoryView,
    DeleteCategoryView,            
)

urlpatterns = [
    
    path("list/",CategoriesListView.as_view(),name="category-list"),
    path("details/<slug:slug>/",CategoriesDetailsView.as_view(),name="category-details"),
    path("crate/",CreateCategoryView.as_view(),name="catrgory-create"),
    path("update/<slug:slug>/",UpdateCategoryView.as_view(),name="category-update"),
    path("delete/<slug:slug>/",DeleteCategoryView.as_view(),name="category-delete"),
]
