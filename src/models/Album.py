from src.models.Carta import Carta
from src.models.Carta import generar_llave_identificadora
import json
from src.managers.CardDataManager import cargar_cartas_desde_json
jso = json.JSONDecoder()



class node:
    def __init__(self, Carta):
        self.Carta = Carta
        self.next = None


class Album:
    def __init__(self):
        self.size = 0
        self.head = None
        self.getcartascreadas()

    #Agrega una nueva carta al álbum
    def add(self, Carta):
        newNode = node(Carta)
        if self.head is None:
            self.head = newNode
            self.size += 1
            return
        current_node = self.head
        while (current_node.next):
            current_node = current_node.next

        current_node.next = newNode
        self.size += 1

    def obtener_cartas(self):
        """Método para obtener todas las cartas en formato de lista"""
        cartas = []
        current_node = self.head
        while current_node is not None:
            cartas.append(current_node.Carta)
            current_node = current_node.next
        return cartas

    # Función para leer el archivo JSON y asignar los atributos a variables
    def getcartascreadas(self):
        # Cargar cartas desde el JSON y asignarlas a variables
        cargar_cartas_desde_json()
        for l in cargar_cartas_desde_json():
            print(l)
            self.add(l)

    def sorter(self):
        """Método para ordenar las cartas por el nombre_personaje y nombre_variante"""
        cartas = self.obtener_cartas()
        cartas_ordenadas = sorted(cartas, key=lambda carta: (carta.nombre_personaje, carta.nombre_variante))
        self.head = None
        for carta in cartas_ordenadas:
            self.add(carta)

    def clean(self):
        self.head = None

    def getcard(self, posicion):
        current = self.head
        i = 1
        if posicion > self.size:
            print("Posicion mayor que el tamaño del album")
            return
        if posicion < 1:
            print("La posicion debe ser 1 o mayor")
            return

        while i <= posicion:
            if i == posicion:
                return current.Carta
            current = current.next
            i += 1
        return
    #Verifica si todas las cartas en el álbum están activas en el juego.
    def albumvalid(self):
        current = self.head
        i = 0
        while i > self.size:
            if not current.Carta.activa_en_juego:
                return False
        return True

    def to_list(self):
        """Convierte el Album a una lista de diccionarios de cartas."""
        return [carta.to_dict() for carta in self.obtener_cartas()]

    @classmethod
    def from_list(cls, data_list, isdeck):
        """Crea un Album a partir de una lista de diccionarios de cartas."""
        album = cls(isdeck)
        album.clean()
        for carta_data in data_list:
            carta = Carta.from_dict(carta_data)
            album.add(carta)
        return album

class playerAlbum(Album):

    def __init__(self, isdeck):
        super().__init__()
        self.isdeck = isdeck
        self.llave = self.llave4deck()

    def getcartascreadas(self):
        pass

    def llave4deck(self):
        if self.isdeck > 0:
            return generar_llave_identificadora
        else:
            return