import socket

connections = {}


stophilo = False
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def start_server(port=5555):
    global stophilo
    global server
    stophilo = False
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', port))
    print("Servidor de emparejamiento en ejecución en el puerto", port)

    while not stophilo:
        # Recibe la clave de emparejamiento del cliente
        data, addr = server.recvfrom(1024)
        key = data.decode()

        if key in connections:
            # Emparejamiento con el cliente existente
            peer_addr = connections.pop(key)

            # Enviar direcciones mutuamente
            server.sendto(f"{peer_addr[0]}:{peer_addr[1]}".encode(), addr)
            server.sendto(f"{addr[0]}:{addr[1]}".encode(), peer_addr)
            print(f"Clientes emparejados: {addr} <--> {peer_addr}")
        else:
            # Guardar dirección del cliente y enviar mensaje de espera
            connections[key] = addr
            server.sendto("WAIT".encode(), addr)
            print(f"Esperando segundo cliente para emparejar con {addr}")

def stop():
    global stophilo
    stophilo = True
    server.close()