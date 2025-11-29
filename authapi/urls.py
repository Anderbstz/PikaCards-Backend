from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("profile/", views.profile),   # <--- NUEVO
    path("change-password/", views.change_password),
    path("delete-account/", views.delete_account),
    
]