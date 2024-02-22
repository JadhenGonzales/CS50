
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routes
    path("create_post", views.create_post, name="create_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("follow_profile", views.follow_profile, name="follow_profile"),
    path("like_post", views.like_post, name="like_post"),
    path("posts/", views.posts, name="posts"),
    path("posts/<str:category>", views.posts, name="posts"),
]
