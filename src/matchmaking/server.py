import socket

# Constantes globales
SERVER_HOST = "0.0.0.0"  # Dirección del servidor (escucha en todas las interfaces)
SERVER_PORT = 5555       # Puerto del servidor
RECV_BUFFER_SIZE = 1024  # Tamaño del buffer para recibir datos
WAIT_MESSAGE = "WAIT"    # Mensaje de espera para los clientes

# Variables globales
connections = {}  # Diccionario para almacenar conexiones pendientes
stophilo = False
server = None


def start_server():
    """
    Inicia el servidor de emparejamiento.
    """
    global stophilo
    global server

    stophilo = False
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    print(f"Servidor de emparejamiento en ejecución en el puerto {SERVER_PORT}")

    while not stophilo:
        try:
            # Recibe la clave de emparejamiento del cliente
            data, addr = server.recvfrom(RECV_BUFFER_SIZE)
            key = data.decode()

            if key == "cleanthis":
                # Eliminar la entrada del cliente actual si existe
                if addr in connections.values():
                    # Encontrar la clave asociada a la dirección y eliminarla
                    key_to_remove = [k for k, v in connections.items() if v == addr]
                    for k in key_to_remove:
                        del connections[k]
                    print(f"Dirección {addr} eliminada de las conexiones.")
                else:
                    print(f"No se encontró la dirección {addr} en las conexiones.")
                continue

            if key in connections:
                # Emparejar con un cliente existente
                peer_addr = connections.pop(key)

                # Enviar direcciones mutuamente
                server.sendto(f"{peer_addr[0]}:{peer_addr[1]}".encode(), addr)
                server.sendto(f"{addr[0]}:{addr[1]}".encode(), peer_addr)
                print(f"Clientes emparejados: {addr} <--> {peer_addr}")
            else:
                # Guardar dirección del cliente y enviar mensaje de espera
                connections[key] = addr
                server.sendto(WAIT_MESSAGE.encode(), addr)
                print(f"Esperando segundo cliente para emparejar con {addr}")
        except socket.error as e:
            print(f"Error del socket: {e}")
            break


def stop():
    """
    Detiene el servidor de emparejamiento.
    """
    global stophilo
    global server

    stophilo = True
    if server:
        server.close()
        print("Servidor detenido.")


