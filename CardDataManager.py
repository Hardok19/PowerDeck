import json
from Carta import Carta
import os
import random

archivo = 'cards.json'
PROBABILIDADES_RAREZA = {
    "Ultra-Rara": 0.05,
    "Muy Rara": 0.12,
    "Rara": 0.18,
    "Normal": 0.25,
    "Básica": 0.40
}

# Función para guardar cartas en un archivo JSON, evitando sobrescribir el archivo
def guardar_cartas_en_json(cartas):
    cartas_a_guardar = []
    # Verifica si el archivo existe, y si existe, carga su contenido
    if os.path.exists(archivo):
        with open(archivo, 'r') as archivo_json:
            try:
                cartas_existentes = json.load(archivo_json)
            except json.JSONDecodeError:
                # Si el archivo está vacío o malformado, lo ignoramos y seguimos con una lista vacía
                pass

    # Agrega las nuevas cartas a la lista de cartas a guardar
    for carta in cartas:
        temp = {
            "nombre_personaje": carta.nombre_personaje,
            "descripcion": carta.descripcion,
            "nombre_variante": carta.nombre_variante,
            "es_variante": carta.es_variante,
            "raza": carta.raza,
            "Selección de raza": carta.selecRaza,
            "imagen": carta.imagen,
            "tipo_carta": carta.tipo_carta,
            "turno_poder": carta.turno_poder,
            "bonus_poder": carta.bonus_poder,
            "atributos": carta.atributos,
            "Poder total": carta.poder_total,
            "fecha de creacion": f"{carta.fecha_creacion}",
            "fecha de modificacion": f"{carta.fecha_modificacion}"

        }


        cartas_a_guardar.append(temp)

    # Guarda la lista de cartas en formato JSON en el archivo especificado
    with open(archivo, 'w') as archivo_json:
        json.dump(cartas_a_guardar, archivo_json, indent=4)

# Función para cargar las cartas desde un archivo JSON
def cargar_cartas_desde_json():
    """ Carga una lista de objetos Carta desde un archivo JSON.
    Si el archivo no existe, retorna una lista vacía."""
    try:
        with open(archivo, 'r') as archivo_json:
            cartas_datos = json.load(archivo_json)
            cartas = []
            for carta_dato in cartas_datos:
                carta = Carta(
                    nombre_personaje=carta_dato["nombre_personaje"],
                    descripcion=carta_dato["descripcion"],
                    nombre_variante=carta_dato["nombre_variante"],
                    es_variante=carta_dato["es_variante"],
                    selecRaza="",
                    raza=carta_dato["raza"],
                    imagen=carta_dato["imagen"],
                    tipo_carta=carta_dato["tipo_carta"],
                    turno_poder=carta_dato["turno_poder"],
                    bonus_poder=carta_dato["bonus_poder"],
                    atributos=carta_dato["atributos"]
                )
                cartas.append(carta)
            print(f"Cartas cargadas desde {archivo}")
            return cartas
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}, se retornará una lista vacía.")
        return []

# Función para leer el archivo JSON y asignar los atributos a variables
def leer_cartas_y_guardar_en_variables():
    """ Lee las cartas desde el archivo JSON y asigna cada atributo a una variable local.
    Imprime información básica de cada carta leída."""
    try:
        with open(archivo, 'r') as archivo_json:
            cartas_datos = json.load(archivo_json)

            for carta_dato in cartas_datos:
                # Asignar cada atributo de la carta a una variable
                nombre_personaje = carta_dato["nombre_personaje"]
                descripcion = carta_dato["descripcion"]
                nombre_variante = carta_dato["nombre_variante"]
                es_variante = carta_dato["es_variante"]
                raza = carta_dato["raza"]
                imagen = carta_dato["imagen"]
                tipo_carta = carta_dato["tipo_carta"]
                turno_poder = carta_dato["turno_poder"]
                bonus_poder = carta_dato["bonus_poder"]
                atributos = carta_dato["atributos"]


                print(f"Carta: {nombre_personaje}, Raza: {raza}, Turno de poder: {turno_poder}")

    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}.")


def asignar_cartas_iniciales(album, cantidad_cartas=10):
    cartas_asignadas = []
    tipos_asignados = set()  # Para asegurar que no haya duplicados por personaje

    # Obtener todas las cartas disponibles
    todas_cartas = album.obtener_cartas()

    # Filtrar cartas por rareza según las probabilidades
    cartas_por_tipo = {
        tipo: [carta for carta in todas_cartas if carta.tipo_carta == tipo]
        for tipo in PROBABILIDADES_RAREZA
    }

    # Asignación de cartas según probabilidades
    while len(cartas_asignadas) < cantidad_cartas:
        # Elegir un tipo de carta basado en la probabilidad
        tipo_carta = random.choices(
            population=list(PROBABILIDADES_RAREZA.keys()),
            weights=list(PROBABILIDADES_RAREZA.values()),
            k=1
        )[0]

        # Seleccionar una carta del tipo seleccionado
        cartas_disponibles = [
            carta for carta in cartas_por_tipo[tipo_carta]
            if carta.nombre_personaje not in tipos_asignados
        ]

        if cartas_disponibles:
            carta_seleccionada = random.choice(cartas_disponibles)
            cartas_asignadas.append(carta_seleccionada)
            tipos_asignados.add(carta_seleccionada.nombre_personaje)  # Marcar el personaje como asignado

    return cartas_asignadas