from django.urls.conf import path

from courses_app import views

urlpatterns = [
    path(
        "courses",
        views.list_courses,
        name=views.list_courses.__name__,
    ),
]
