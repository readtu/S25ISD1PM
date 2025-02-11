from django.urls import path

from chairs_app import views

urlpatterns = [
    path("", views.home, name=views.home.__name__),
]
