from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Base de datos simulada en memoria
todos = {
    "todos": ['Estudiar', 'Comer', 'Jugar UNO']
}

@app.route("/", methods=["GET"])
def home():
    """
    Ruta raíz de la API.
    Retorna un mensaje simple para indicar que el servicio está activo.
    """
   # return "Simple TODO API"
   

@app.route("/todos", methods=["GET"])
def select_todos():
    """
    Obtener todos los TODOs.
    Retorna un JSON con la lista actual de tareas.
    """
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def create_todo():
    """
    Crear un nuevo TODO.
    Espera un JSON con el campo 'todo'.
    
    Ejemplo:
    {
        "todo": "Hacer ejercicio"
    }
    """
    data = request.json
    if not data or "todo" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    todos["todos"].append(data['todo'])
    return jsonify({"message": "Nuevo TODO creado"}), 201

@app.route("/todos", methods=["DELETE"])
def delete_todo():
    """
    Eliminar un TODO existente.
    Espera un JSON con el campo 'todo' que debe coincidir exactamente.
    
    Ejemplo:
    {
        "todo": "Comer"
    }
    """
    data = request.json
    if not data or "todo" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    todo_item = data['todo']
    if todo_item not in todos["todos"]:
        return jsonify({"error": "TODO no encontrado"}), 404

    todos["todos"].remove(todo_item)
    return jsonify({"message": f"TODO '{todo_item}' eliminado"}), 200

@app.route("/todos", methods=["PUT"])
def update_todo():
    """
    Actualizar un TODO existente.
    Espera un JSON con los campos 'old' y 'new'.
    
    Ejemplo:
    {
        "old": "Estudiar",
        "new": "Estudiar Flask"
    }
    """
    data = request.json
    if not data or "old" not in data or "new" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    old_todo = data['old']
    new_todo = data['new']

    if old_todo not in todos["todos"]:
        return jsonify({"error": "TODO a actualizar no encontrado"}), 404

    index = todos["todos"].index(old_todo)
    todos["todos"][index] = new_todo

    return jsonify({"message": f"TODO actualizado de '{old_todo}' a '{new_todo}'"}), 200

if __name__ == "__main__":
    app.run(debug=True)
