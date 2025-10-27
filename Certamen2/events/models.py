from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    location = models.CharField(max_length=250)
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capacity = models.PositiveIntegerField()

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return self.title

    @property
    def seats_taken(self):
        return self.registrations.count()

    @property
    def seats_available(self):
        return max(self.capacity - self.seats_taken, 0)

    @property
    def revenue(self):
        return self.registrations.count() * self.price

    def is_past(self):
        return self.start_datetime < timezone.now()

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [UniqueConstraint(fields=["user","event"], name="unique_user_event_registration")]
