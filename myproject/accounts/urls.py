from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signup/success/", views.signup_success, name="signup_success"),
    path("edit/<str:user_id>/", views.edit_user, name="edit_user"),
    path("delete/<str:user_id>/", views.delete_user, name="delete_user"),
]
