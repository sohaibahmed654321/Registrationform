from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test_firebase, name="test_firebase"),
    path("", views.home, name="home"),       # 👈 pehle wala home
    path("signup/", views.signup, name="signup"),
    path("signup/success/", views.signup_success, name="signup_success"),
    path("edit/<str:user_id>/", views.edit_user, name="edit_user"),
    path("delete/<str:user_id>/", views.delete_user, name="delete_user"),
    path("login/", views.login_view, name="login"),
]