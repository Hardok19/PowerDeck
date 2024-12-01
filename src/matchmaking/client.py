import socket
import time
import threading

# Constantes globales
SERVER_IP = "127.0.0.1"  #IP
SERVER_PORT = 5555
DEFAULT_KEY = "12345"
MAX_WAIT_TIME = 10
RECV_BUFFER_SIZE = 1024
TIMEOUT = 1  # Tiempo de espera en segundos para recibir datos

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def connect_to_peer(key, server_ip, server_port=SERVER_PORT, max_wait_time=MAX_WAIT_TIME):
    # Enviar clave al servidor
    client.sendto(key.encode(), (server_ip, server_port))
    start_time = time.time()
    while True:
        try:
            client.settimeout(TIMEOUT)
            data, _ = client.recvfrom(RECV_BUFFER_SIZE)
            response = data.decode()
            if response == "WAIT":
                print("Esperando otro cliente para emparejar...")
                if time.time() - start_time > max_wait_time:
                    print("No se encontraron oponentes.")
                    return None, None
                time.sleep(1)
            else:
                peer_ip, peer_port = response.split(':')
                print(f"Emparejado con IP: {peer_ip}, Puerto: {peer_port}")
                return peer_ip, int(peer_port)
        except socket.timeout:
            if time.time() - start_time > max_wait_time:
                print("No se encontraron oponentes.")
                client.sendto("cleanthis".encode(), (server_ip, server_port))
                return None, None
            pass

def listen_to_peer(peer_address):
    while True:
        try:
            data, _ = client.recvfrom(RECV_BUFFER_SIZE)
            if data:
                mensaje = data.decode()
                print(f"Mensaje del par: {mensaje}")
                # Aquí puedes procesar el mensaje recibido
        except:
            break

def iniciar_emparejamiento(partida_encontrada):
    # Conectar al servidor para obtener la IP y puerto del par
    client_ip, client_port = connect_to_peer(DEFAULT_KEY, SERVER_IP)
    if client_ip is None:
        # No se encontró oponente
        partida_encontrada.set()
        partida_encontrada.result = False
        return
    print(f"Listo para comunicar con par en {client_ip}:{client_port}")
    # Emparejamiento exitoso
    partida_encontrada.set()
    partida_encontrada.result = True
    # Ahora, establecer conexión con el par
    peer_address = (client_ip, client_port)
    # Iniciar hilo para escuchar mensajes
    hilo_escucha = threading.Thread(target=listen_to_peer, args=(peer_address,))
    hilo_escucha.start()

def listen(client_socket):
    print("Esperando mensajes...")
    while True:
        # Recibir mensajes del otro cliente
        message, _ = client_socket.recvfrom(RECV_BUFFER_SIZE)
        if message:
            print(f"Mensaje recibido: {message.decode()}")
        time.sleep(0.1)
