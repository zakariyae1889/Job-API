from django.urls import path

from .views import (
    RegisterUserView,
    
    UpdateProfileView,
    DeleteProfileView,
    ChangePasswordView,
  
    CurrentUsersView,
    LogoutView
)


urlpatterns = [
    
    path("register/",RegisterUserView.as_view(),name="authentication-register"),

    path("update/",UpdateProfileView.as_view(),name="authentication-update"),
    path("delete/",DeleteProfileView.as_view(),name="authentication-delete"),
    path("change-password/",ChangePasswordView.as_view() , name="authentication-changepassword"),
    path("profile/",CurrentUsersView.as_view(),name="authentication-profile"),
    path("logout/",LogoutView.as_view(),name="authentication-logout")

]
