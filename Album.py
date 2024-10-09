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


    def getcartascreadas(self):
        with open('cards.json', 'r') as f:
            data = json.load(f)

        for cards in data["cartas"]:
            actual = Carta(cards["nombre_personaje"], cards["descripcion"], cards["nombre_variante"], cards["es_variante"],
                           cards["raza"], cards["tipo_carta"], cards["SeleccionCarta"], cards["activa_en_juego"],
                           cards["activa_en_sobres"], cards["turno_poder"], cards["bonus_poder"], cards["atributos"])
            actual.poder_total = cards["poder_total"]
            actual.llave_identificadora = cards["llave_identificadora"]
            actual.fecha_creacion = cards["fecha_creacion"]
            actual.fecha_modificacion = cards["fecha_modificacion"]
            self.add(actual)
        print("")



