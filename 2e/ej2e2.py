"""
Enunciado:
Desarrolla una aplicación web con Flask que explore los diferentes tipos MIME (Multipurpose Internet Mail Extensions)
y cómo enviar diversos formatos de contenido en respuestas HTTP. Esta aplicación te permitirá entender
cómo configurar correctamente los encabezados Content-Type para diferentes tipos de datos.

Los tipos MIME son fundamentales en el desarrollo web ya que indican al cliente (navegador, aplicación, etc.)
cómo interpretar y mostrar los datos enviados por el servidor. Una API bien diseñada debe utilizar
los tipos MIME apropiados para cada tipo de contenido.

Tu aplicación debe implementar los siguientes endpoints:

1. `GET /text`: Devuelve un texto plano con el tipo MIME `text/plain`.
   - Ejemplo de uso: Enviar mensajes simples o logs sin formato.

2. `GET /html`: Devuelve un fragmento HTML con el tipo MIME `text/html`.
   - Ejemplo de uso: Enviar contenido que debe ser renderizado como una página web.

3. `GET /json`: Devuelve un objeto JSON con el tipo MIME `application/json`.
   - Ejemplo de uso: Intercambio de datos estructurados entre cliente y servidor en APIs RESTful.

4. `GET /xml`: Devuelve un documento XML con el tipo MIME `application/xml`.
   - Ejemplo de uso: APIs SOAP, configuraciones o intercambio de datos estructurados en formato XML.

5. `GET /image`: Devuelve una imagen con el tipo MIME `image/png`.
   - Ejemplo de uso: Servir imágenes directamente desde la API.

6. `GET /binary`: Devuelve datos binarios con el tipo MIME `application/octet-stream`.
   - Ejemplo de uso: Descargar archivos como PDFs, archivos comprimidos o cualquier contenido binario genérico.

Tu tarea es completar la implementación de la función create_app() y de los endpoints solicitados,
asegurándote de utilizar el tipo MIME correcto en cada caso y generar el contenido adecuado.

Esta actividad te enseñará cómo configurar correctamente los tipos de contenido en respuestas HTTP,
una habilidad esencial para el desarrollo de APIs y servicios web que manejan diferentes formatos de datos.
"""

import io
import os

from flask import Flask, Response, jsonify, make_response, send_file


def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route("/text", methods=["GET"])
    def get_text():
        """
        Devuelve un texto plano con el tipo MIME `text/plain`
        """
        return Response("Este es un texto plano", content_type="text/plain")

    @app.route("/html", methods=["GET"])
    def get_html():
        """
        Devuelve un fragmento HTML con el tipo MIME `text/html`
        """
        return Response("<h1>Este es un fragmento HTML</h1>", content_type="text/html")

    @app.route("/json", methods=["GET"])
    def get_json():
        """
        Devuelve un objeto JSON con el tipo MIME `application/json`
        """
        return Response(
            '{"mensaje": "Este es un objeto JSON"}', content_type="application/json"
        )

    @app.route("/xml", methods=["GET"])
    def get_xml():
        """
        Devuelve un documento XML con el tipo MIME `application/xml`
        """
        return Response(
            "<mensaje>Este es un documento XML</mensaje>",
            content_type="application/xml",
        )

    @app.route("/image", methods=["GET"])
    def get_image():
        """
        Devuelve una imagen con el tipo MIME `image/png`
        """
        # Crear una imagen PNG simple en memoria
        import base64

        # PNG mínimo válido (1x1 píxel transparente)
        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        )

        return Response(png_data, content_type="image/png")

    @app.route("/binary", methods=["GET"])
    def get_binary():
        """
        Devuelve datos binarios genéricos con el tipo MIME `application/octet-stream`
        Para este ejemplo, puedes crear unos bytes aleatorios o un archivo binario simple
        """
        # Generar datos binarios aleatorios
        binary_data = os.urandom(1024)  # 1KB de datos aleatorios

        response = Response(binary_data, content_type="application/octet-stream")
        response.headers["Content-Disposition"] = "attachment; filename=datos.bin"
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
