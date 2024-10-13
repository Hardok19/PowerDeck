from Carta import Carta
import json
jso = json.JSONDecoder()
from CardDataManager import leer_cartas_y_guardar_en_variables
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
            return
        current_node = self.head
        while (current_node.next):
            current_node = current_node.next

        current_node.next = newNode

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
        leer_cartas_y_guardar_en_variables()



