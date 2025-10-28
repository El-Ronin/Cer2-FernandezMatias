from django.contrib import admin
from .models import Event, Registration

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "datetime", "location", "capacity", "seats_taken", "seats_available", "collected_amount")
    search_fields = ("title", "location")
    list_filter = ("datetime",)
    inlines = [RegistrationInline]

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "created_at")
    search_fields = ("user__username", "event__title")
    list_filter = ("created_at",)
