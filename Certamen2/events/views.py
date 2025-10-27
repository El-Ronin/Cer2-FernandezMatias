from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Event, Registration

class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"

class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        event = self.object
        ctx["already_registered"] = False
        if user.is_authenticated:
            ctx["already_registered"] = Registration.objects.filter(user=user, event=event).exists()
        return ctx

@login_required
def register_to_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.is_past():
        messages.error(request, "No puedes inscribirte a un evento pasado.")
        return redirect("events:event_detail", pk=event.pk)
    with transaction.atomic():
        event = Event.objects.select_for_update().get(pk=pk)
        if Registration.objects.filter(user=request.user, event=event).exists():
            messages.info(request, "Ya estás inscrito en este evento.")
            return redirect("events:event_detail", pk=event.pk)
        if event.seats_available <= 0:
            messages.error(request, "No hay plazas disponibles.")
            return redirect("events:event_detail", pk=event.pk)
        Registration.objects.create(user=request.user, event=event)
        messages.success(request, "Inscripción realizada con éxito.")
    return redirect("events:event_detail", pk=event.pk)

class MyRegistrationsView(LoginRequiredMixin, ListView):
    model = Registration
    template_name = "events/my_registrations.html"
    context_object_name = "registrations"

    def get_queryset(self):
        return Registration.objects.select_related("event").filter(user=self.request.user)

class LegacyIndexView(TemplateView):
    template_name = "legacy/index.html"
class LegacyEventosView(TemplateView):
    template_name = "legacy/eventos.html"
class LegacyComunidadView(TemplateView):
    template_name = "legacy/comunidad.html"
