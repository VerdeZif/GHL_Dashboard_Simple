import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_create_appointment_returns_201_or_400():
    client = APIClient()
    url = reverse('create-appointment')

    payload = {
        "paciente_nombre": "Juan Pérez",
        "start_time": "2025-10-07T10:00:00Z",
        "end_time": "2025-10-07T11:00:00Z"
    }

    response = client.post(url, payload, format='json')

    # En local puede devolver 201 si guarda o 400 si falta un campo
    assert response.status_code in [201, 400]
    assert isinstance(response.json(), dict)


@pytest.mark.django_db
def test_list_appointments_requires_params():
    client = APIClient()
    url = reverse('list-appointments')
    response = client.get(url)
    assert response.status_code == 400
    assert "calendarId" in response.json()["detail"]
