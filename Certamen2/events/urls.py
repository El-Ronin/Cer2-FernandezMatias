from django.urls import path
from . import views

app_name = "events"
urlpatterns = [
    path("", views.EventListView.as_view(), name="event_list"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    path("event/<int:pk>/register/", views.register_to_event, name="register_to_event"),
    path("my-registrations/", views.MyRegistrationsView.as_view(), name="my_registrations"),
    path("legacy/eventos/", views.LegacyEventosView.as_view(), name="legacy_eventos"),
]
