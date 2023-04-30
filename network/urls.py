
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("follow_unfollow/<str:user_name>", views.follow_unfollow, name="follow_unfollow"),
    path("following", views.following, name="following"),
    path("edit/<str:post_id>", views.edit, name="edit"),
    path("likes/<str:post_id>", views.likes, name="likes")
]
