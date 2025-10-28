from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="list"),
    path("<int:pk>/", views.event_detail, name="detail"),
    path("<int:pk>/register/", views.register_event, name="register"),
    path("<int:pk>/cancel/", views.cancel_registration, name="cancel"),
    path("mine/", views.my_events, name="my_events"),  # optional alias
]
