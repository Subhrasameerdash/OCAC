from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),        # homepage
    path("contact/", views.contact, name="contact"),  # contact page
]