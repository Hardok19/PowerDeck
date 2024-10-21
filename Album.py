from Carta import Carta
import json
jso = json.JSONDecoder()



class node:
    def __init__(self, Carta):
        self.Carta = Carta
        self.next = None




class Album:
    def __init__(self, ):
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


