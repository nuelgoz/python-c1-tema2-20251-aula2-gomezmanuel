"""
Enunciado:
Desarrolla una API REST utilizando Flask que permita realizar operaciones básicas sobre una lista de tareas (to-do list).
La API debe exponer los siguientes endpoints:

1. `GET /tasks`: Devuelve la lista completa de tareas.
2. `POST /tasks`: Agrega una nueva tarea. El cuerpo de la solicitud debe incluir un JSON con el campo "name".
3. `DELETE /tasks/<task_id>`: Elimina una tarea específica por su ID.
4. `PUT /tasks/<task_id>`: Actualiza el nombre de una tarea existente por su ID. El cuerpo de la solicitud debe incluir un JSON con el campo "name".

Observa que el mismo endpoint (por ejemplo, `/tasks/<task_id>`) puede recibir diferentes verbos HTTP (DELETE, PUT) y realizar distintas operaciones según el verbo utilizado. Esta es una característica fundamental de las APIs REST.

Requisitos:
- Cada tarea debe tener un ID único (entero) y un nombre (cadena de texto).
- La lista de tareas debe almacenarse en memoria (no es necesario usar una base de datos).
- Maneja errores como intentar eliminar o actualizar una tarea que no existe.

Ejemplo:
Si la lista de tareas inicial está vacía:
1. Una solicitud `POST /tasks` con el cuerpo `{"name": "Comprar leche"}` debe agregar la tarea con ID 1.
2. Una solicitud `GET /tasks` debe devolver `[{"id": 1, "name": "Comprar leche"}]`.
3. Una solicitud `PUT /tasks/1` con el cuerpo `{"name": "Comprar pan"}` debe actualizar la tarea con ID 1.
4. Una solicitud `GET /tasks` debe devolver `[{"id": 1, "name": "Comprar pan"}]`.
5. Una solicitud `DELETE /tasks/1` debe eliminar la tarea con ID 1.
6. Una solicitud `GET /tasks` debe devolver `[]`.

Tu tarea es implementar esta API en Flask.
"""

from flask import Flask, jsonify, request

# Esta lista almacenará todas las tareas
tasks = []
# Este contador se usará para asignar IDs únicos
next_id = 1


def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        """
        Devuelve la lista completa de tareas
        """
        # Implementa este endpoint
        return jsonify(tasks)

    @app.route("/tasks", methods=["POST"])
    def add_task():
        """
        Agrega una nueva tarea
        El cuerpo de la solicitud debe incluir un JSON con el campo "name"
        """
        # Implementa este endpoint
        global next_id
        data = request.get_json()

        if not data or "name" not in data:
            return jsonify({"error": "Task name is required"}), 400

        task = {"id": next_id, "name": data["name"]}
        tasks.append(task)
        next_id += 1

        return jsonify(task), 201

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        """
        Elimina una tarea específica por su ID
        """
        # Implementa este endpoint
        global tasks
        task_to_delete = None
        for task in tasks:
            if task["id"] == task_id:
                task_to_delete = task
                break

        if task_to_delete is None:
            return jsonify({"error": "Task not found"}), 404

        tasks = [task for task in tasks if task["id"] != task_id]
        return jsonify({"message": "Task deleted"}), 200

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        """
        Actualiza el nombre de una tarea existente por su ID
        El cuerpo de la solicitud debe incluir un JSON con el campo "name"
        Código de estado: 200 - OK si se actualizó, 404 - Not Found si no existe
        """
        # Implementa este endpoint
        data = request.get_json()

        if not data or "name" not in data:
            return jsonify({"error": "Task name is required"}), 400

        task_to_update = None
        for task in tasks:
            if task["id"] == task_id:
                task_to_update = task
                break

        if task_to_update is None:
            return jsonify({"error": "Task not found"}), 404

        task_to_update["name"] = data["name"]
        return jsonify(task_to_update), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
