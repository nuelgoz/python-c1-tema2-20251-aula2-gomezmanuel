"""
Enunciado:
Desarrolla una aplicación web con Flask que demuestre diferentes formas de pasar parámetros a una API.
La aplicación debe implementar los siguientes endpoints:

1. `GET /search`: Acepta parámetros de consulta (query parameters) en la URL.
   Ejemplo: `/search?q=flask&category=tutorial`
   Debe devolver los parámetros recibidos en formato JSON.

2. `POST /form`: Acepta datos de formulario (form data) en el cuerpo de la petición.
   Debe devolver los datos recibidos en formato JSON.

3. `POST /json`: Acepta datos JSON en el cuerpo de la petición.
   Debe devolver los datos recibidos en formato JSON.

Esta actividad te enseñará las diferentes formas de recibir parámetros en una aplicación Flask:
- Parámetros de consulta en la URL (query parameters)
- Datos de formulario (form data)
- Datos JSON en el cuerpo de la petición

Estos métodos son fundamentales para construir APIs web interactivas que puedan recibir información del cliente.
"""

from flask import Flask, jsonify, request

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/search', methods=['GET'])
    def search():
        """
        Maneja parámetros de consulta (query parameters) en la URL
        Ejemplo: /search?q=flask&category=tutorial

        Acceso mediante request.args (diccionario con los parámetros de la URL)
        """
        # Implementa este endpoint para obtener los parámetros de consulta
        # y devolverlos en formato JSON
        query_params = request.args.to_dict()
        return jsonify(query_params)

    @app.route('/form', methods=['POST'])
    def form_handler():
        """
        Maneja datos de formulario enviados mediante POST

        Acceso mediante request.form (para datos de formulario)
        """
        # Implementa este endpoint para obtener los datos del formulario
        # y devolverlos en formato JSON
        form_data = request.form.to_dict()
        return jsonify(form_data)

    @app.route('/json', methods=['POST'])
    def json_handler():
        """
        Maneja datos JSON enviados en el cuerpo de la petición

        Acceso mediante request.get_json() (para datos JSON)
        """
        # Implementa este endpoint para obtener los datos JSON
        # y devolverlos en formato JSON
        json_data = request.get_json()
        return jsonify(json_data)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
