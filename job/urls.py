from django.urls import path
from .views import (JobListView,JobDetailsView,CreateJobView,UpdateJobView,JobDeleteView)

urlpatterns = [
    path("list/",JobListView.as_view(),name="job-list"),
    path("details/<slug:slug>/",JobDetailsView.as_view(),name="job"),
    path("create/",CreateJobView.as_view(),name="job-create"),
    path("update/<slug:slug>/",UpdateJobView.as_view(),name="job-update"),
    path("delete/<slug:slug>/",JobDeleteView.as_view(),name="job-delete")
]
