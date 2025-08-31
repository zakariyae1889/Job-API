from django.urls import path
from .views import (
    ApplicationListView,EmployeeApplicationListView,EmployeeApplicationUpdateStatusView,
    JobSeekerApplyView,UpdateJobSeekerApplyView,DeleteJobSeekerApplyView
)
urlpatterns = [
    
    path("<slug:slug>/apply/",JobSeekerApplyView.as_view(), name="apply-job"),
    path("list-job-seeker/",ApplicationListView.as_view(),name="list-job-seeker"),
    path("list-employee/",EmployeeApplicationListView.as_view(),name="llist-employee"),
    path("<slug:slug>/status/",EmployeeApplicationUpdateStatusView.as_view(),name="status-application"),
    path("<slug:slug>/update/",UpdateJobSeekerApplyView.as_view(), name="update-application"),
    path("<slug:slug>/delete/",DeleteJobSeekerApplyView.as_view(), name="delete-application"),
]
