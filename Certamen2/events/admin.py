from django.contrib import admin
from django.db.models import Count
from .models import Event, Registration
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title","start_datetime","location","capacity","seats_available_display","revenue_display")
    search_fields = ("title","location")
    list_filter = ("start_datetime",)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_reg_count=Count("registrations"))
    @admin.display(description="Plazas disp.")
    def seats_available_display(self, obj: Event):
        return obj.seats_available
    @admin.display(description="Recaudación")
    def revenue_display(self, obj: Event):
        return f"$ {obj.revenue:,.0f}"
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user","event","created_at")
