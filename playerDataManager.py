import json
import os

archivo_jugadores = "players.json"

def cargar_jugadores():
    # Si el archivo no existe, retorna una lista vacía
    if not os.path.exists(archivo_jugadores):
        return []

    # Intenta cargar el archivo JSON, maneja excepciones si el archivo está vacío o malformado
    with open(archivo_jugadores, 'r') as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            # Retorna una lista vacía si el archivo está vacío o malformado
            print("Advertencia: El archivo players.json está vacío o malformado. Se inicializará una lista vacía.")
            return []

def guardar_jugador(jugador):
    jugadores = cargar_jugadores()

    # Verificar si el alias o correo ya existen
    for j in jugadores:
        if j["alias"] == jugador["alias"] or j["correo"] == jugador["correo"]:
            return False, "El alias o correo ya están registrados."

    # Agregar el nuevo jugador a la lista de jugadores
    jugadores.append(jugador)
    # Guardar la lista actualizada en el archivo JSON
    with open(archivo_jugadores, 'w') as archivo:
        json.dump(jugadores, archivo, indent=4)
    return True, "Jugador registrado correctamente."