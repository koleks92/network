
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
<<<<<<< HEAD
    path("<str:user>", views.profile, name="profile")
=======
    path("<str:user_name>", views.profile, name="profile")
>>>>>>> parent of 84bc927 (Profile Follows/Followers)
]
