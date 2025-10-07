import requests
import time
from django.conf import settings
import calendar
import datetime

def to_millis(dt: datetime.datetime) -> int:
    """
    Convierte un datetime a timestamp en milisegundos (UTC).
    """
    return int(calendar.timegm(dt.utctimetuple()) * 1000)


BASE = settings.GHL_BASE_URL.rstrip('/')
TOKEN = settings.GHL_PRIVATE_TOKEN
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Version": "2021-04-15"
}

def create_appointment_in_ghl(calendar_id, contact_id, title, start_dt_iso, end_dt_iso, time_zone='America/Lima', notes=None):
    url = f"{BASE}/calendars/events/appointments"
    payload = {
        "calendarId": calendar_id,
        "locationId": settings.GHL_LOCATION_ID,
        "contactId": contact_id,
        "title": title,
        "startTime": start_dt_iso,
        "endTime": end_dt_iso,
        "meetingLocationType": "custom",
        "appointmentStatus": "confirmed",
        "description": notes or ""
    }
    r = requests.post(url, headers=HEADERS, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()

import time

def list_calendar_appointments(calendar_id: str, start_time: int, end_time: int, location_id: str = None):
    """
    Lista las citas de un calendario en GHL usando la API oficial.
    :param calendar_id: ID del calendario
    :param start_time: timestamp en milisegundos (13 dígitos)
    :param end_time: timestamp en milisegundos (13 dígitos)
    :param location_id: ID de la location (si no lo pasas, lo toma de settings)
    """
    if not location_id:
        location_id = settings.GHL_LOCATION_ID  # asegúrate de tenerlo en tu settings.py

    url = f"{BASE}/calendars/events"
    params = {
        "locationId": location_id,
        "calendarId": calendar_id,
        "startTime": start_time,
        "endTime": end_time,
    }

    resp = requests.get(url, headers=HEADERS, params=params, timeout=20)

    # si falla, lanza la excepción para que tu vista la capture
    resp.raise_for_status()

    return resp.json()