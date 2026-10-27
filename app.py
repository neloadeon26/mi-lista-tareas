from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
ARCHIVO = "tareas.json"

# --- Funciones para manejar el archivo JSON ---
def cargar_tareas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return []

def guardar_tareas(tareas):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(tareas, archivo, indent=4, ensure_ascii=False)

# --- Rutas de la aplicación web ---

# Página principal: muestra las tareas
@app.route("/")
def index():
    tareas = cargar_tareas()
    return render_template("index.html", tareas=tareas)

# Ruta para añadir una tarea
@app.route("/add", methods=["POST"])
def add():
    tareas = cargar_tareas()
    nueva_tarea = request.form.get("tarea")
    if nueva_tarea:
        tareas.append({"descripcion": nueva_tarea, "completada": False})
        guardar_tareas(tareas)
    return redirect(url_for("index"))

# Ruta para marcar como completada
@app.route("/complete/<int:index>")
def complete(index):
    tareas = cargar_tareas()
    if 0 <= index < len(tareas):
        tareas[index]["completada"] = True
        guardar_tareas(tareas)
    return redirect(url_for("index"))

# Ruta para eliminar una tarea
@app.route("/delete/<int:index>")
def delete(index):
    tareas = cargar_tareas()
    if 0 <= index < len(tareas):
        tareas.pop(index)
        guardar_tareas(tareas)
    return redirect(url_for("index"))

if __name__ == "__main__":
    # host="0.0.0.0" permite que otros dispositivos (como tu móvil) se conecten
    app.run(host="0.0.0.0", port=5000, debug=True)