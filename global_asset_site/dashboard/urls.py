from django.urls import path

from . import auth, views

urlpatterns = [
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("queries/", views.query_list, name="query_list"),
    path("queries/<int:number>/", views.query_detail, name="query_detail"),
    path("operations/", views.operations, name="operations"),
    path("tables/<str:table>/", views.table_view, name="table_view"),
    path("manage/", views.manage, name="manage"),
]
