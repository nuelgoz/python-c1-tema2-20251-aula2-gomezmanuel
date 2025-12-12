"""
Enunciado:
Desarrolla una aplicación web con Flask que demuestre diferentes formas de acceder a la
información enviada en las solicitudes HTTP. Esta aplicación te permitirá entender cómo
procesar diferentes tipos de datos proporcionados por los clientes.

Tu aplicación debe implementar los siguientes endpoints:

1. `GET /headers`: Devuelve los encabezados (headers) de la solicitud en formato JSON.
   - Muestra información como User-Agent, Accept-Language, etc.

2. `GET /browser`: Analiza el encabezado User-Agent y devuelve información sobre:
   - El navegador que está usando el cliente
   - El sistema operativo
   - Si es un dispositivo móvil o no

3. `POST /echo`: Acepta cualquier tipo de datos y devuelve exactamente los mismos datos
   en la misma forma que fueron enviados. Debe manejar:
   - JSON
   - Datos de formulario (form data)
   - Texto plano

4. `POST /validate-id`: Valida un documento de identidad según estas reglas:
   - Debe recibir un JSON con un campo "id_number"
   - El ID debe tener exactamente 9 caracteres
   - Los primeros 8 caracteres deben ser dígitos
   - El último carácter debe ser una letra
   - Devuelve JSON indicando si es válido o no

Esta actividad te enseñará cómo acceder y manipular datos de las solicitudes HTTP,
una habilidad fundamental para crear APIs robustas y aplicaciones web interactivas.
"""

import re

from flask import Flask, jsonify, request


def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route("/headers", methods=["GET"])
    def get_headers():
        """
        Devuelve los encabezados (headers) de la solicitud en formato JSON.
        Convierte el objeto headers de la solicitud en un diccionario.
        """
        # Implementa este endpoint:
        # 1. Accede a los encabezados de la solicitud usando request.headers
        # 2. Convierte los encabezados a un formato adecuado para JSON
        # 3. Devuelve los encabezados como respuesta JSON

        # Convertir headers a diccionario
        headers_dict = dict(request.headers)
        return jsonify(headers_dict)

    @app.route("/browser", methods=["GET"])
    def get_browser_info():
        """
        Analiza el encabezado User-Agent y devuelve información sobre el navegador,
        sistema operativo y si es un dispositivo móvil.
        """
        # Implementa este endpoint:
        # 1. Obtén el encabezado User-Agent de request.headers
        # 2. Analiza la cadena para detectar:
        #    - El nombre del navegador (Chrome, Firefox, Safari, etc.)
        #    - El sistema operativo (Windows, macOS, Android, iOS, etc.)
        #    - Si es un dispositivo móvil (detecta cadenas como "Mobile", "Android", "iPhone")
        # 3. Devuelve la información como respuesta JSON

        user_agent = request.headers.get("User-Agent", "")

        # Detectar navegador
        browser = "Unknown"
        if "Chrome" in user_agent:
            browser = "Chrome"
        elif "Firefox" in user_agent:
            browser = "Firefox"
        elif "Safari" in user_agent and "Chrome" not in user_agent:
            browser = "Safari"
        elif "Edge" in user_agent:
            browser = "Edge"

        # Detectar sistema operativo (priorizar dispositivos móviles)
        os = "Unknown"
        if "iPhone" in user_agent or "iPad" in user_agent:
            os = "iOS"
        elif "Android" in user_agent:
            os = "Android"
        elif "Windows" in user_agent:
            os = "Windows"
        elif "Mac OS X" in user_agent or "Macintosh" in user_agent:
            os = "macOS"
        elif "Linux" in user_agent:
            os = "Linux"

        # Detectar si es móvil
        is_mobile = any(
            mobile in user_agent for mobile in ["Mobile", "Android", "iPhone", "iPad"]
        )

        return jsonify({"browser": browser, "os": os, "is_mobile": is_mobile})

    @app.route("/echo", methods=["POST"])
    def echo():
        """
        Devuelve exactamente los mismos datos que recibe.
        Debe detectar el tipo de contenido y procesarlo adecuadamente.
        """
        # Implementa este endpoint:
        # 1. Detecta el tipo de contenido de la solicitud con request.content_type
        # 2. Según el tipo de contenido, extrae los datos:
        #    - Para JSON: usa request.get_json()
        #    - Para form data: usa request.form
        #    - Para texto plano: usa request.data
        # 3. Devuelve los mismos datos con el mismo tipo de contenido

        content_type = request.content_type or ""

        if "application/json" in content_type:
            # Para JSON, devolver el mismo JSON
            return jsonify(request.get_json())
        elif (
            "application/x-www-form-urlencoded" in content_type
            or "multipart/form-data" in content_type
        ):
            # Para form data, devolver como JSON
            return jsonify(dict(request.form))
        elif "text/plain" in content_type:
            # Para texto plano, devolver el mismo texto
            return request.data, 200, {"Content-Type": "text/plain"}
        else:
            # Para otros tipos, devolver los datos como están
            return request.data

    @app.route("/validate-id", methods=["POST"])
    def validate_id():
        """
        Valida un documento de identidad según reglas específicas:
        - Debe tener exactamente 9 caracteres
        - Los primeros 8 caracteres deben ser dígitos
        - El último carácter debe ser una letra
        """
        # Implementa este endpoint:
        # 1. Obtén el campo "id_number" del JSON enviado
        # 2. Valida que cumpla con las reglas especificadas
        # 3. Devuelve un JSON con el resultado de la validación

        # Verificar que el contenido sea JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()

        # Verificar que existe el campo requerido
        if "id_number" not in data:
            return jsonify({"error": "Missing required field 'id_number'"}), 400

        id_number = data["id_number"]

        # Validar que es una cadena
        if not isinstance(id_number, str):
            return jsonify({"error": "id_number must be a string"}), 400

        # Validar longitud exacta de 9 caracteres
        if len(id_number) != 9:
            return jsonify(
                {"valid": False, "error": "ID must have exactly 9 characters"}
            ), 200

        # Validar que los primeros 8 caracteres son dígitos
        if not id_number[:8].isdigit():
            return jsonify(
                {"valid": False, "error": "First 8 characters must be digits"}
            ), 200

        # Validar que el último carácter es una letra
        if not id_number[-1].isalpha():
            return jsonify(
                {"valid": False, "error": "Last character must be a letter"}
            ), 200

        # Si todas las validaciones pasan
        return jsonify({"valid": True}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
