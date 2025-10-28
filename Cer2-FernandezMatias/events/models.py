from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    """Modelo principal de eventos."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.datetime.strftime('%d/%m/%Y %H:%M')}"

    @property
    def seats_taken(self):
        """Número de entradas vendidas / inscripciones confirmadas."""
        return self.registrations.count()

    @property
    def seats_available(self):
        """Número de asientos disponibles."""
        return max(self.capacity - self.seats_taken, 0)

    @property
    def collected_amount(self):
        """Monto total recaudado = precio × cantidad de inscritos."""
        return self.seats_taken * self.price

    @property
    def is_full(self):
        """Indica si el evento está lleno."""
        return self.seats_taken >= self.capacity

    class Meta:
        ordering = ["-datetime"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class Registration(models.Model):
    """Inscripciones a eventos (1 usuario -> 1 evento)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
