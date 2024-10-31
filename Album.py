from Carta import Carta
import json
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
        from CardDataManager import cargar_cartas_desde_json
        # Cargar cartas desde el JSON y asignarlas a variables
        cargar_cartas_desde_json()
        for l in cargar_cartas_desde_json():
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
    def albumvalid(self):
        current = self.head
        i = 0
        while i > self.size:
            if not current.Carta.activa_en_juego:
                return False
        return True

class playerAlbum(Album):
    def __init__(self):
        super().__init__()

    def getcartascreadas(self):
        pass

