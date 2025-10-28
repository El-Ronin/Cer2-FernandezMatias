from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone

from .models import Event, Registration
from .forms import SignUpForm
from django.contrib.auth.models import User

# lista de eventos
def event_list(request):
    events = Event.objects.all()
    return render(request, "events/event_list.html", {"events": events})

# detalle de eventos
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    already_registered = False
    if request.user.is_authenticated:
        already_registered = Registration.objects.filter(user=request.user, event=event).exists()
    return render(request, "events/event_detail.html", {"event": event, "already_registered": already_registered})

# sign up
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data["password"],
            )
            login(request, user)
            messages.success(request, "Cuenta creada con éxito. ¡Bienvenido!")
            return redirect("events:list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

# Registro para evento
@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.seats_available <= 0:
        messages.error(request, "No hay plazas disponibles para este evento.")
        return redirect("events:detail", pk=pk)
    reg, created = Registration.objects.get_or_create(user=request.user, event=event)
    if not created:
        messages.info(request, "Ya estás registrado en este evento.")
    else:
        messages.success(request, "Registro realizado con éxito.")
    return redirect("events:detail", pk=pk)

# cancelar registro
@login_required
def cancel_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    Registration.objects.filter(user=request.user, event=event).delete()
    messages.success(request, "Tu inscripción ha sido anulada.")
    return redirect("events:my_events")

# mis eventos
@login_required
def my_events(request):
    regs = Registration.objects.filter(user=request.user).select_related("event")
    return render(request, "events/my_events.html", {"registrations": regs})
