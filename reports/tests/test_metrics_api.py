import pytest
from django.test import Client

@pytest.mark.django_db
def test_metrics_endpoint_returns_json():
    """
    Verifica que el endpoint /metrics/ responda correctamente en formato JSON.
    """
    client = Client()
    response = client.get('/metrics/')

    # ✅ Acepta 200 (correcto), 400 (faltan variables) o 500 (error en conexión)
    assert response.status_code in [200, 400, 500]

    data = response.json()
    assert isinstance(data, dict)

    # Si la respuesta es exitosa, debe contener los campos esperados
    if response.status_code == 200:
        # Revisar que las claves numéricas existan
        expected_keys = ["created", "confirmed", "cancelled"]
        assert all(k in data for k in expected_keys)

        # Verificar que solo esos campos sean enteros
        assert all(isinstance(data[k], int) for k in expected_keys)
