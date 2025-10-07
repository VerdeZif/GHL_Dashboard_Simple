from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CitaSerializer
from .models import Cita
from .ghl_services import create_appointment_in_ghl, list_calendar_appointments, to_millis
import datetime


class AppointmentCreateView(APIView):
    def post(self, request):
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            cita = serializer.save()
            
            # Llamada a GHL
            try:
                create_appointment_in_ghl(
                    calendar_id=request.data.get("calendarId"),
                    contact_id=request.data.get("contactId"),
                    title=cita.paciente_nombre,
                    start_dt_iso=cita.start_time.isoformat(),
                    end_dt_iso=cita.end_time.isoformat(),
                    notes=cita.notas
                )
            except Exception as e:
                return Response({
                    "detail": "Error creando appointment en GHL",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response(CitaSerializer(cita).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AppointmentListView(APIView):
    def get(self, request):
        calendar_id = request.query_params.get("calendarId")
        start_date = request.query_params.get("startDate")  # YYYY-MM-DD
        end_date = request.query_params.get("endDate")      # YYYY-MM-DD

        if not calendar_id or not start_date or not end_date:
            return Response({
                "detail": "calendarId, startDate y endDate son obligatorios (YYYY-MM-DD)."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            start_time = to_millis(start_dt)
            end_time = to_millis(end_dt)

            data = list_calendar_appointments(calendar_id, start_time, end_time)
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "detail": "Error listando citas del calendario en GHL",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)