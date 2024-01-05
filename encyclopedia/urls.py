from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("add", views.add, name="add"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random", views.random, name="random")
]
