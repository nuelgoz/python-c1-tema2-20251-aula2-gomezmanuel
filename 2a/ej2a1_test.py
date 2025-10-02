import pytest
import threading
import requests
import time
from ej2a1 import create_server

@pytest.fixture
def server():
    """
    Fixture para iniciar y detener el servidor HTTP durante las pruebas
    """
    # Crear el servidor en un puerto específico para pruebas
    server = create_server(host="localhost", port=8888)

    # Iniciar el servidor en un hilo separado
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # Esperar un momento para que el servidor se inicie
    time.sleep(0.5)

    yield server

    # Detener el servidor después de las pruebas
    server.shutdown()
    server.server_close()
    thread.join(1)

def test_root_endpoint(server):
    """
    Prueba el endpoint / para validar que devuelve el mensaje correcto.
    """
    response = requests.get("http://localhost:8888/")
    assert response.status_code == 200, "El código de estado debe ser 200."
    # Comparing the exact bytes representation rather than the string
    assert "Hola mundo" in response.text, "El mensaje debe contener 'Hola mundo'."

def test_nonexistent_endpoint(server):
    """
    Prueba un endpoint que no existe para validar que devuelve un código de error 404.
    """
    response = requests.get("http://localhost:8888/nonexistent")
    assert response.status_code == 404, "El código de estado debe ser 404 para rutas inexistentes."
