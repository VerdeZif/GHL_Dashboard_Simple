import pytest
from django.test import Client

@pytest.mark.django_db
def test_dashboard_view_loads_html():
    """
    Verifica que la vista del dashboard se cargue correctamente y devuelva HTML válido.
    """
    client = Client()
    response = client.get('/dashboard/')

    # ✅ Debe responder con 200
    assert response.status_code == 200

    # ✅ Tipo de contenido debe ser HTML
    assert "text/html" in response["Content-Type"]

    # ✅ Debe contener el título del dashboard
    content = response.content.decode("utf-8")
    assert "Dashboard de Métricas GHL" in content
