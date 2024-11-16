import socket
import threading
import time


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def connect_to_peer(key, server_ip, server_port=5555):
    # Enviar clave al servidor
    client.sendto(key.encode(), (server_ip, server_port))

    # Esperar respuesta del servidor para el emparejamiento
    while True:
        data, _ = client.recvfrom(1024)
        response = data.decode()

        if response == "WAIT":
            print("Esperando otro cliente para emparejar...")
            time.sleep(1)  # Espera breve antes de reintentar
        else:
            peer_ip, peer_port = response.split(':')
            print(f"Emparejado con IP: {peer_ip}, Puerto: {peer_port}")
            return peer_ip, int(peer_port)
def iniciar_emparejamiento(partida_encontrada):
    key = "12345"
    server_ip = "127.0.0.1"  # Se debe cambiar a la IP del servidor si está en otra máquina

    # Conectar al servidor para obtener la IP y puerto del par
    client_ip, client_port = connect_to_peer(key, server_ip)
    print(f"Listo para comunicar con par en {client_ip}:{client_port}")

    # Cuando el emparejamiento es exitoso, marcamos el evento
    partida_encontrada.set()


def listen(client_socket):
    print("Esperando mensajes...")
    while True:
        # Recibir mensajes del otro cliente
        message, _ = client_socket.recvfrom(1024)
        if message:
            print(f"Mensaje recibido: {message.decode()}")
        time.sleep(0.1)

