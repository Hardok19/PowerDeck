import pygame
import pygame_gui
from PowerDeck.src.models.Album import playerAlbum
import re
from PowerDeck.src.ui.Gwindows import mostrar_ventana_advertencia, mostrar_album
from PowerDeck.src.managers.CardDataManager import asignar_cartas_iniciales
from PowerDeck.src.managers.playerDataManager import save_players

# Definimos algunas constantes
ANCHO_VENTANA = 1366
ALTO_VENTANA = 720
FPS = 60
cantidad_cartas = 10  # Configurable, cantidad de cartas iniciales


def addplayer(name, alias, pais, correo, contra, album):
    mensaje = ""
    result = True
    dar = True
    patron = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'

    # Validaciones de entrada
    if pais == "":
        mensaje = "Debe seleccionar su país"
        dar = False
        result = False
    if correo == "" or contra == "":
        mensaje = "Se deben llenar todos los campos requeridos"
        dar = False
        result = False

    if not len(name) in range(4, 12) or not len(alias) in range(4, 12):
        mensaje = "El nombre y alias deben estar entre 4 y 12 caracteres"
        dar = False
        result = False
    if not re.match(patron, correo):
        mensaje = "Inserte un email válido"
        dar = False
        result = False

    # Asignación de cartas iniciales si todos los datos son correctos
    if dar:
        cartas_iniciales = asignar_cartas_iniciales(album, cantidad_cartas=cantidad_cartas)
        albumplayer = playerAlbum()

        # Agregar las cartas iniciales al álbum del jugador
        for carta in cartas_iniciales:
            albumplayer.add(carta)

        mazos = []
        print(f"Cartas iniciales asignadas al jugador {name}: {cartas_iniciales}")

        # Mostrar mensaje de éxito
        mensaje = "Jugador registrado exitosamente"
        return result, [name, alias, pais, correo, contra, albumplayer, mazos], mensaje
    else:
        # Retornar en caso de error
        return result, None, mensaje


def playermenu(player, indexP, manager, players):
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

    mazos = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(508, 200, 350, 100),
        text='Ver Mazos',
        manager=manager
    )
    crearmazo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(508, 400, 350, 100),
        text='Crear Mazo',
        manager=manager
    )
    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == crearmazo:
                manager.clear_and_reset()
                players = nuevomazo(player[5], indexP, manager, players, max_seleccion=cantidad_cartas)
                ejecutando = False
                playermenu(player, indexP, manager, players)
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == mazos:
                manager.clear_and_reset()
                vermazos(indexP, players)
                ejecutando = False
                playermenu(player, indexP, manager, players)

            manager.process_events(evento)

        # Actualización y renderizado
        manager.update(tiempo_delta)
        pantalla.fill((0, 25, 50))  # Fondo azul oscuro
        manager.draw_ui(pantalla)

        pygame.display.flip()
    manager.clear_and_reset()


def mostrar_cardsforuser(playeralbum, manager):
    pantalla = pygame.display.set_mode((1000, 600))
    font = pygame.font.SysFont(None, 20)
    font2 = pygame.font.SysFont(None, 35)
    asignadas = font2.render(f"Se te han asignado estas {str(cantidad_cartas)} cartas", True, (100, 100, 255))

    imagen_ancho = 100
    imagen_alto = 150

    continuar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(400, 450, 200, 50),
        text='Continuar',
        manager=manager
    )

    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == continuar:
                ejecutando = False
            manager.process_events(evento)

        pantalla.fill((0, 25, 0))  # Fondo verde oscuro

        cartax = 200

        # Mostrar las cartas asignadas
        for i in range(1, cantidad_cartas + 1):
            carta = playeralbum.getcard(i)
            try:
                imagen_carta = pygame.image.load(carta.imagen)
                imagen_carta = pygame.transform.scale(imagen_carta, (imagen_ancho, imagen_alto))
                pantalla.blit(imagen_carta, (cartax, 200))
                pantalla.blit(font.render(carta.nombre_personaje, True, (100, 100, 255)), (cartax, 350))
                cartax += 175
            except pygame.error as e:
                print(f"Error al cargar la imagen {carta.imagen}: {e}")
        pantalla.blit(asignadas,
                      asignadas.get_rect(center=[pantalla.get_rect().centerx, pantalla.get_rect().centery - 180]))

        # Actualización y renderizado
        manager.update(tiempo_delta)
        manager.draw_ui(pantalla)
        pygame.display.flip()


# Función para mostrar álbum y selección múltiple de cartas al crear un mazo
def nuevomazo(playeralbum, indexP, manager, players, max_seleccion=cantidad_cartas):
    playeralbum.sorter()
    mostrar_variantes = True

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Añadir Mazo")
    label_nombre = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((700, 20), (300, 30)),
                                               text='Nombre del mazo',
                                               manager=manager)

    entrada_nombre = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((700, 50), (300, 30)),
                                                         manager=manager)

    addmazo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(750, 90, 200, 50),
        text='Añadir Mazo',
        manager=manager
    )

    # Coordenadas y dimensiones para mostrar cartas
    x_offset = 50
    y_offset = 50
    imagen_ancho = 100
    imagen_alto = 150
    texto_espacio_vertical = 30
    carta_espacio_vertical = imagen_alto + 120

    boton_rect = pygame.Rect(ANCHO_VENTANA - 150, 10, 130, 40)
    reloj = pygame.time.Clock()
    ejecutando = True
    scroll_position = 0
    scroll_speed = 30

    # Obtener cartas y procesar para mostrar
    try:
        cartas_a_mostrar = playeralbum.obtener_cartas()
        if not mostrar_variantes:
            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if
                                carta.es_variante == "No" or carta.es_variante == False]
    except Exception as e:
        print("Error al cargar cartas:", e)
        cartas_a_mostrar = []

    cartas_seleccionadas = []
    total_altura_cartas = len(cartas_a_mostrar) * carta_espacio_vertical + y_offset
    contenido_visible = ALTO_VENTANA
    contenido_total = total_altura_cartas if total_altura_cartas > contenido_visible else contenido_visible

    scrollbar_altura = max(ALTO_VENTANA * (contenido_visible / contenido_total), 30)
    scrollbar_pos_x = ANCHO_VENTANA - 20
    scrollbar_width = 15

    while ejecutando:
        tiempo_delta = reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    mostrar_variantes = not mostrar_variantes
                    try:
                        cartas_a_mostrar = playeralbum.obtener_cartas()
                        if not mostrar_variantes:
                            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if carta.es_variante == "No"]
                    except Exception as e:
                        print("Error al actualizar cartas:", e)
                        cartas_a_mostrar = []
                    total_altura_cartas = len(cartas_a_mostrar) * carta_espacio_vertical + y_offset
                    contenido_total = total_altura_cartas if total_altura_cartas > contenido_visible else contenido_visible
                    scrollbar_altura = max(ALTO_VENTANA * (contenido_visible / contenido_total), 30)

                # Manejo de selección de cartas
                for idx, carta in enumerate(cartas_a_mostrar):
                    carta_pos = y_offset + (idx * carta_espacio_vertical) - scroll_position
                    carta_rect = pygame.Rect(x_offset, carta_pos, imagen_ancho, imagen_alto)
                    if carta_rect.collidepoint(evento.pos):
                        if carta in cartas_seleccionadas:
                            cartas_seleccionadas.remove(carta)
                        elif len(cartas_seleccionadas) < max_seleccion:
                            cartas_seleccionadas.append(carta)
                        break
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == addmazo:
                continuar = True
                if not len(cartas_seleccionadas) == cantidad_cartas:
                    mostrar_ventana_advertencia(manager, f"seleccione {cantidad_cartas} cartas")
                    continue
                for al in players[indexP - 1][6]:
                    if al[0] == entrada_nombre.get_text():
                        mostrar_ventana_advertencia(manager, "Un mazo con ese nombre ya existe en tus mazos")
                        continuar = False
                if entrada_nombre.get_text() == "":
                    mostrar_ventana_advertencia(manager, "Ingrese un nombre para el mazo")
                    continuar = False
                if not continuar: continue
                temp = playerAlbum()
                for card in cartas_seleccionadas:
                    temp.add(card)
                players[indexP - 1][6].append((entrada_nombre.get_text(), temp))
                save_players(players)
                print("Mazo agregado correctamente")
                ejecutando = False
                manager.clear_and_reset()
                nuevomazo(playeralbum, indexP, manager, players, max_seleccion=cantidad_cartas)

            # Scroll con rueda del mouse
            if evento.type == pygame.MOUSEWHEEL:
                scroll_increment = -evento.y * scroll_speed
                scroll_position = max(0, min(scroll_position + scroll_increment, contenido_total - contenido_visible))
            manager.process_events(evento)

        pantalla.fill((24, 0, 40))
        pygame.draw.rect(pantalla, (0, 255, 0), boton_rect)
        fuente = pygame.font.SysFont(None, 24)
        boton_texto = "Ver Variantes" if not mostrar_variantes else "Ocultar Variantes"
        pantalla.blit(fuente.render(boton_texto, True, (0, 0, 0)), (boton_rect.x + 10, boton_rect.y + 10))

        # Dibujar cartas
        for idx, carta in enumerate(cartas_a_mostrar):
            carta_pos = y_offset + (idx * carta_espacio_vertical) - scroll_position

            if carta_pos > -carta_espacio_vertical and carta_pos < ALTO_VENTANA:
                try:
                    imagen_carta = pygame.image.load(carta.imagen)
                    imagen_carta = pygame.transform.scale(imagen_carta, (imagen_ancho, imagen_alto))
                    pantalla.blit(imagen_carta, (x_offset, carta_pos))
                    if carta in cartas_seleccionadas:
                        pygame.draw.rect(pantalla, (255, 0, 0),
                                         pygame.Rect(x_offset, carta_pos, imagen_ancho, imagen_alto), 3)
                except pygame.error as e:
                    print(f"Error al cargar la imagen {carta.imagen}: {e}")

                pantalla.blit(fuente.render(f"Personaje: {carta.nombre_personaje}", True, (255, 255, 255)),
                              (x_offset + imagen_ancho + 20, carta_pos))

        scrollbar_pos_y = (scroll_position / (contenido_total - contenido_visible + 1)) * (
                ALTO_VENTANA - scrollbar_altura)
        pygame.draw.rect(pantalla, (200, 200, 200),
                         (scrollbar_pos_x, scrollbar_pos_y, scrollbar_width, scrollbar_altura))

        manager.update(tiempo_delta)
        manager.draw_ui(pantalla)
        pygame.display.update()
    manager.clear_and_reset()
    return players


def vermazos(indexP, players):
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    player = players[indexP - 1]
    font = pygame.font.Font(None, 36)
    reloj = pygame.time.Clock()
    ejecutando = True

    albumes = player[6]  # Suponiendo que player[6] es una lista de tuplas (nombre, Album)

    while ejecutando:
        pantalla.fill((30, 30, 30))  # Fondo gris oscuro

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, (nombre, album) in enumerate(albumes):
                    rect = pygame.Rect(50, 50 + i * 40, 200, 30)
                    if rect.collidepoint(mouse_pos):
                        mostrar_album(album)

        for i, (nombre, album) in enumerate(albumes):
            valid = "Válido" if album.albumvalid() else "Inválido"
            texto = font.render(nombre, True, (255, 255, 255))
            valido = font.render(valid, True, (255, 255, 255))
            rect = pygame.Rect(50, 50 + i * 40, 200, 30)
            pygame.draw.rect(pantalla, (70, 70, 200), rect)
            pantalla.blit(texto, (rect.x + 10, rect.y + 5))
            pantalla.blit(valido, (rect.x + 200, rect.y + 5))

        pygame.display.flip()
        reloj.tick(FPS)