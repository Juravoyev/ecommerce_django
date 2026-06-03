from django.urls import path

from apps.common import views


urlpatterns = [
    path("", views.home, name="home"),
]