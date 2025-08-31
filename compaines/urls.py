from django.urls import path
from .views import (CompaniesListView,CompanyDetailsView,CreateCompanyView,UpdateCompanyView,DeleteCompanyView)

urlpatterns = [
    
    path("list/",CompaniesListView.as_view(),name="companies-list"),
    path("details/<slug:slug>/",CompanyDetailsView.as_view(),name="company-details"),
    path("create/",CreateCompanyView.as_view(),name="company-create"),
    path("update/<slug:slug>/",UpdateCompanyView.as_view(),name="company-update"),
    path("delete/<slug:slug>/",DeleteCompanyView.as_view(),name="company-delete")
]
