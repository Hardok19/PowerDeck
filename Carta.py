from datetime import datetime
import random
import string


# Función para generar una llave única
def generar_llave_identificadora():
    identificador_carta = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    identificador_variante = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    return f"C-{identificador_carta}-V-{identificador_variante}"


# Clase para representar una carta
class Carta:
    def __init__(self, nombre_personaje, descripcion, nombre_variante, es_variante, raza, imagen, tipo_carta,
                 selecRaza, turno_poder, bonus_poder, atributos):
        self.nombre_personaje = nombre_personaje
        self.descripcion = descripcion
        self.nombre_variante = nombre_variante
        self.es_variante = es_variante
        self.fecha_creacion = datetime.now()
        self.fecha_modificacion = self.fecha_creacion
        self.raza = raza
        self.imagen = imagen
        self.tipo_carta = tipo_carta
        self.selecRaza = selecRaza
        self.activa_en_juego = True
        self.activa_en_sobres = True
        self.turno_poder = turno_poder
        self.bonus_poder = bonus_poder
        self.atributos = atributos
        self.poder_total = sum(self.atributos.values())
        self.llave_identificadora = generar_llave_identificadora()

    # Representación en texto de la carta
    def __repr__(self):
        return f"Personaje: {self.nombre_personaje} - Variante: {self.nombre_variante} - Raza: {self.raza}"

