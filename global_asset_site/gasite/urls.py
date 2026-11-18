# Sends every web address to the dashboard app

from django.urls import include, path

urlpatterns = [path("", include("dashboard.urls"))]
