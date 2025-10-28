from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("my-events/", views.my_events, name="my_events"),
]
