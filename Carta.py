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

    #Método para obtener el nombre del peronaje
    def get_nombrepersonaje(self):
        return self.nombre_personaje

    # Representación en texto de la carta
    def __repr__(self):
        return f"Personaje: {self.nombre_personaje} - Variante: {self.nombre_variante} - Raza: {self.raza}"

    def to_dict(self):
        return {
            'nombre_personaje': self.nombre_personaje,
            'descripcion': self.descripcion,
            'nombre_variante': self.nombre_variante,
            'es_variante': self.es_variante,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_modificacion': self.fecha_modificacion.isoformat(),
            'raza': self.raza,
            'imagen': self.imagen,
            'tipo_carta': self.tipo_carta,
            'selecRaza': self.selecRaza,
            'activa_en_juego': self.activa_en_juego,
            'activa_en_sobres': self.activa_en_sobres,
            'turno_poder': self.turno_poder,
            'bonus_poder': self.bonus_poder,
            'atributos': self.atributos,
            'poder_total': self.poder_total,
            'llave_identificadora': self.llave_identificadora
        }

    @classmethod
    def from_dict(cls, data):
        data['fecha_creacion'] = datetime.fromisoformat(data['fecha_creacion'])
        data['fecha_modificacion'] = datetime.fromisoformat(data['fecha_modificacion'])
        carta = cls(
            nombre_personaje=data['nombre_personaje'],
            descripcion=data['descripcion'],
            nombre_variante=data['nombre_variante'],
            es_variante=data['es_variante'],
            raza=data['raza'],
            imagen=data['imagen'],
            tipo_carta=data['tipo_carta'],
            selecRaza=data['selecRaza'],
            turno_poder=data['turno_poder'],
            bonus_poder=data['bonus_poder'],
            atributos=data['atributos']
        )
        carta.fecha_creacion = data['fecha_creacion']
        carta.fecha_modificacion = data['fecha_modificacion']
        carta.activa_en_juego = data.get('activa_en_juego', True)
        carta.activa_en_sobres = data.get('activa_en_sobres', True)
        carta.poder_total = data['poder_total']
        carta.llave_identificadora = data['llave_identificadora']
        return carta