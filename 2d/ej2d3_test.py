import pytest
from flask import Flask
from flask.testing import FlaskClient
from ej2d3 import create_app
import logging
from io import StringIO


class LogCaptureHandler(logging.Handler):
    """
    Manejador personalizado para capturar mensajes de log durante las pruebas
    """
    def __init__(self):
        super().__init__()
        self.logs = StringIO()
        self.setLevel(logging.INFO)
        self.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    def emit(self, record):
        """Añade un mensaje de log a los logs capturados"""
        self.logs.write(self.format(record) + '\n')

    def get_logs(self):
        """Devuelve los logs capturados y reinicia"""
        logs = self.logs.getvalue()
        self.logs = StringIO()
        return logs

@pytest.fixture
def client() -> FlaskClient:
    app: Flask = create_app()
    app.testing = True

    # Configurar el capturador de logs
    log_capture = LogCaptureHandler()
    app.logger.addHandler(log_capture)
    app.logger.setLevel(logging.INFO)

    with app.test_client() as client:
        client.log_capture = log_capture
        yield client

def test_get_animals(client):
    """Test GET /animals - should return all animals"""
    response = client.get("/animals")
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[0]["name"] == "León"

def test_get_animal_exists(client):
    """Test GET /animals/1 - should return the animal with ID 1"""
    response = client.get("/animals/1")
    assert response.status_code == 200
    assert response.json["name"] == "León"
    assert response.json["species"] == "Panthera leo"

def test_get_animal_not_found(client):
    """Test GET /animals/999 - should return 404 error"""
    response = client.get("/animals/999")
    assert response.status_code == 404
    assert "error" in response.json or "message" in response.json

    # Verificar que se registró el error en los logs
    logs = client.log_capture.get_logs()
    assert "INFO:" in logs, "Debe registrarse un mensaje de nivel INFO para errores 404"

def test_add_animal(client):
    """Test POST /animals with valid data - should add a new animal"""
    response = client.post("/animals", json={"name": "Tigre", "species": "Panthera tigris"})
    assert response.status_code == 201
    assert response.json["name"] == "Tigre"
    assert response.json["id"] == 4

def test_add_animal_invalid(client):
    """Test POST /animals with invalid data - should return 400 error"""
    response = client.post("/animals", json={"name": "Tigre"})  # Missing species
    assert response.status_code == 400
    assert "error" in response.json or "message" in response.json

    # Verificar que se registró el error en los logs
    logs = client.log_capture.get_logs()
    assert "WARNING:" in logs, "Debe registrarse un mensaje de nivel WARNING para errores 400"

def test_delete_animal(client):
    """Test DELETE /animals/2 - should delete the animal with ID 2"""
    response = client.delete("/animals/2")
    assert response.status_code == 204

    # Verify animal was deleted
    response = client.get("/animals/2")
    assert response.status_code == 404

def test_delete_animal_not_found(client):
    """Test DELETE /animals/999 - should return 404 error"""
    response = client.delete("/animals/999")
    assert response.status_code == 404
    assert "error" in response.json or "message" in response.json

    # Verificar que se registró el error en los logs
    logs = client.log_capture.get_logs()
    assert "INFO:" in logs, "Debe registrarse un mensaje de nivel INFO para errores 404"

def test_method_not_allowed(client):
    """Test PUT /animals - should return 405 error"""
    response = client.put("/animals")
    assert response.status_code == 405
    assert "error" in response.json or "message" in response.json

    # Verificar que se registró el error en los logs
    logs = client.log_capture.get_logs()
    assert "WARNING:" in logs, "Debe registrarse un mensaje de nivel WARNING para errores 405"

# def test_internal_server_error(client):
#     """Test GET /test-error - should return 500 error"""
#     response = client.get("/test-error")
#     assert response.status_code == 500
#     assert "error" in response.json or "message" in response.json
#
#     # Verificar que se registró el error en los logs
#     logs = client.log_capture.get_logs()
#     assert "ERROR:" in logs, "Debe registrarse un mensaje de nivel ERROR para errores 500"
#     assert "test-error" in logs, "El log debe incluir información de la ruta que causó el error"

