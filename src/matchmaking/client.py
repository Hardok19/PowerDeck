import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def connect_to_peer(key, server_ip, server_port=5555, max_wait_time=10):
    # Enviar clave al servidor
    client.sendto(key.encode(), (server_ip, server_port))
    start_time = time.time()
    while True:
        try:
            client.settimeout(1)  # Esperar 1 segundo por respuesta
            data, _ = client.recvfrom(1024)
            response = data.decode()
            if response == "WAIT":
                print("Esperando otro cliente para emparejar...")
                if time.time() - start_time > max_wait_time:
                    print("No se encontraron oponentes.")
                    return None, None
                time.sleep(1)  # Espera breve antes de reintentar
            else:
                peer_ip, peer_port = response.split(':')
                print(f"Emparejado con IP: {peer_ip}, Puerto: {peer_port}")
                return peer_ip, int(peer_port)
        except socket.timeout:
            if time.time() - start_time > max_wait_time:
                print("No se encontraron oponentes.")
                return None, None
            pass

def iniciar_emparejamiento(partida_encontrada):
    key = "12345"
    server_ip = "127.0.0.1"  # Cambia esto si el servidor está en otra IP

    # Conectar al servidor para obtener la IP y puerto del par
    client_ip, client_port = connect_to_peer(key, server_ip)
    if client_ip is None:
        # No se encontró oponente
        partida_encontrada.set()
        partida_encontrada.result = False  # Indicamos que no se encontró partida
        return
    print(f"Listo para comunicar con par en {client_ip}:{client_port}")
    # Emparejamiento exitoso
    partida_encontrada.set()
    partida_encontrada.result = True  # Indicamos que se encontró partida


def listen(client_socket):
    print("Esperando mensajes...")
    while True:
        # Recibir mensajes del otro cliente
        message, _ = client_socket.recvfrom(1024)
        if message:
            print(f"Mensaje recibido: {message.decode()}")
        time.sleep(0.1)


