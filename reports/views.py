from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import requests
import datetime
import calendar
from datetime import timezone
from collections import defaultdict


def to_millis(dt: datetime.datetime) -> int:
    """Convierte datetime a timestamp en milisegundos (UTC)."""
    return int(calendar.timegm(dt.utctimetuple()) * 1000)


# --- MÉTRICAS DESDE GHL ---
def appointments_metrics(request):
    """
    Devuelve métricas completas desde GHL:
    - Totales (creadas, confirmadas, canceladas)
    - Serie diaria (para líneas y barras)
    - Datos adicionales (scatter y bubble)
    """
    api_key = settings.GHL_PRIVATE_TOKEN
    base_url = settings.GHL_BASE_URL.rstrip('/')
    calendar_id = settings.GHL_CALENDAR_ID
    location_id = settings.GHL_LOCATION_ID

    # Validar configuración
    if not all([api_key, base_url, calendar_id, location_id]):
        return JsonResponse({"error": "Faltan variables en settings (.env)."}, status=400)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": "2021-07-28",
    }

    # Rango de fechas
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")
    days_str = request.GET.get("days")

    if start_str and end_str:
        try:
            start_dt = datetime.datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            end_dt = datetime.datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return JsonResponse({"error": "Formato de fecha inválido. Usa YYYY-MM-DD"}, status=400)
    else:
        end_dt = datetime.datetime.now(timezone.utc)
        days = int(days_str) if days_str else 7
        start_dt = end_dt - datetime.timedelta(days=days)

    start_time = to_millis(start_dt)
    end_time = to_millis(end_dt)

    url = f"{base_url}/calendars/events"
    params = {
        "locationId": location_id,
        "calendarId": calendar_id,
        "startTime": start_time,
        "endTime": end_time,
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        if r.status_code != 200:
            return JsonResponse({
                "error": f"Error desde GHL ({r.status_code})",
                "raw": r.text
            }, status=r.status_code)

        data = r.json()
        events = data.get("events", [])

        # ---------------------------
        # Totales
        # ---------------------------
        created = len(events)
        confirmed = sum(1 for e in events if e.get("appointmentStatus") == "confirmed")
        cancelled = sum(1 for e in events if e.get("appointmentStatus") == "cancelled")

        # ---------------------------
        # Serie diaria + datos extra
        # ---------------------------
        daily_counts = defaultdict(lambda: {"created": 0, "confirmed": 0, "cancelled": 0})
        scatter_data, bubble_data = [], []

        for e in events:
            timestamp = e.get("startTime")
            if not timestamp:
                continue

            dt = datetime.datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).date()
            status = e.get("appointmentStatus", "created").lower()
            duration = e.get("durationMinutes", 0)
            value = e.get("price", 0) or duration

            daily_counts[dt]["created"] += 1
            if status == "confirmed":
                daily_counts[dt]["confirmed"] += 1
            elif status == "cancelled":
                daily_counts[dt]["cancelled"] += 1

            # Scatter: hora vs duración
            try:
                start = datetime.datetime.fromtimestamp(e["startTime"] / 1000, tz=timezone.utc)
                scatter_data.append({
                    "x": start.hour,
                    "y": duration
                })
                # Bubble: día vs duración, tamaño proporcional
                bubble_data.append({
                    "x": start.day,
                    "y": duration,
                    "r": max(3, min(value / 10, 30))
                })
            except:
                continue

        # Convertir serie diaria a lista
        daily_data = [
            {"date": d.strftime("%Y-%m-%d"), **v}
            for d, v in sorted(daily_counts.items())
        ]

        return JsonResponse({
            "created": created,
            "confirmed": confirmed,
            "cancelled": cancelled,
            "daily_data": daily_data,
            "scatter_data": scatter_data,
            "bubble_data": bubble_data,
            "start": start_dt.strftime("%Y-%m-%d"),
            "end": end_dt.strftime("%Y-%m-%d")
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# --- DASHBOARD HTML ---
def dashboard_view(request):
    """Renderiza el panel HTML del dashboard."""
    return render(request, "reports/dashboard.html")
