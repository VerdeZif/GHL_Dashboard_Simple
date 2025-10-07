from django.db import models
from django.utils import timezone

class Cita(models.Model):
    paciente_nombre = models.CharField(max_length=200, default="Paciente Desconocido")
    paciente_email = models.EmailField(blank=True, null=True)
    paciente_telefono = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    notas = models.TextField(blank=True, null=True)

    ghl_event_id = models.CharField(max_length=200, blank=True, null=True)
    ghl_contact_id = models.CharField(max_length=200, blank=True, null=True)
    ghl_synced = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.paciente_nombre} - {self.start_time}"
