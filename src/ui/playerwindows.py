import threading
import pygame
import pygame_gui
from src.ui.Gwindows import mostrar_ventana_advertencia, mostrar_album
from src.managers.playerDataManager import save_players
from src.models.Carta import generar_llave_identificadora
from src.ui.windowsconfig import ANCHO_VENTANA, ALTO_VENTANA, FPS, manager, album, players, cantidad_cartas
from src.logic.playerlogic import validate_player_data, create_player, create_new_deck
from src.matchmaking.client import iniciar_emparejamiento
from src.ui.windowsconfig import manager

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

def addplayer(name, alias, pais, correo, contra, isadmin):
    # Validar datos del jugador
    valid, mensaje = validate_player_data(name, alias, pais, correo, contra, isadmin)
    if not valid:
        return False, None, mensaje

    # Verificar si el alias o correo ya existen
    for player in players:
        if player.alias == alias or player.email == correo:
            mensaje = "El correo o el alias ya existe"
            return False, None, mensaje

    # Crear el jugador
    new_player = create_player(name, alias, pais, correo, contra, album, isadmin, cantidad_cartas)
    return True, new_player, "Jugador registrado exitosamente"

def newUser(isadmin):
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    font = pygame.font.SysFont(None, 30)
    name = font.render("Nombre de usuario", True, (100, 100, 255))
    Alias = font.render("Alias", True, (100, 100, 255))
    pais = font.render("País", True, (100, 100, 255))
    correo = font.render("Correo", True, (100, 100, 255))
    contra = font.render("Contraseña", True, (100, 100, 255))
    entryname = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((68, 110), (300, 30)),
                                                         manager=manager)
    entryAlias = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((68, 310), (300, 30)),
                                                         manager=manager)

    paisentry = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((68, 510), (200, 30)),
                                                      starting_option="",
                                                      options_list=["", "Argentina", "Perú", "Uruguay", "México", "Costa Rica", "Bolivia"],
                                                      manager=manager)

    entrycorreo = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((798, 110), (300, 30)),
                                                         manager=manager)

    entrycontra = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((798, 310), (300, 30)),
                                                         manager=manager)
    entrycontra.set_text_hidden()

    registrarse = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(825, 550, 250, 50),
        text='Registrarse',
        manager=manager
    )
    country = ""
    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == paisentry:
                    country = evento.text
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == registrarse:
                resultado, tempplayer, mensaje = addplayer_ui(
                    entryname.get_text(),
                    entryAlias.get_text(),
                    country,
                    entrycorreo.get_text(),
                    entrycontra.get_text(),
                    isadmin
                )
                if not resultado:
                    mostrar_ventana_advertencia(manager, mensaje)
                    continue

                players.append(tempplayer)
                save_players(players)
                manager.clear_and_reset()
                if not isadmin:
                    mostrar_cardsforuser(tempplayer.album, manager)
                ejecutando = False
            manager.process_events(evento)
        # Actualización y renderizado
        manager.update(tiempo_delta)
        pantalla.fill((0, 25, 50))  # Fondo azul oscuro
        pantalla.blit(name, name.get_rect(topleft=(70, 70)))
        pantalla.blit(Alias, Alias.get_rect(topleft=(70, 270)))
        pantalla.blit(pais, pais.get_rect(topleft=(70, 470)))
        pantalla.blit(correo, correo.get_rect(topleft=(800, 70)))
        pantalla.blit(contra, contra.get_rect(topleft=(800, 270)))
        manager.draw_ui(pantalla)
        pygame.display.flip()
    manager.clear_and_reset()

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
                selected_cards = cartas_seleccionadas
                deck_name = entrada_nombre.get_text()
                existing_decks = players[indexP - 1].mazos

                success, temp_album = create_new_deck(
                    playeralbum,
                    selected_cards,
                    deck_name,
                    existing_decks,
                    max_seleccion
                )
                if not success:
                    mostrar_ventana_advertencia(manager, temp_album)
                    continue

                # Agregar el nuevo mazo al jugador
                players[indexP - 1].mazos.append((deck_name, temp_album, generar_llave_identificadora()))
                save_players(players)
                print("Mazo agregado correctamente")
                ejecutando = False
                manager.clear_and_reset()
                # Reiniciar la función o volver al menú
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
    albumes = player.mazos
    while ejecutando:
        pantalla.fill((30, 30, 30))  # Fondo gris oscuro
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, (nombre, album, llave) in enumerate(albumes):
                    rect = pygame.Rect(50, 50 + i * 40, 200, 30)
                    if rect.collidepoint(mouse_pos):
                        mostrar_album(album)
        for i, (nombre, album, llave) in enumerate(albumes):
            valid = "Válido" if album.albumvalid() else "Inválido"
            texto = font.render(nombre, True, (255, 255, 255))
            valido = font.render(valid, True, (255, 255, 255))
            rect = pygame.Rect(50, 50 + i * 40, 200, 30)
            pygame.draw.rect(pantalla, (70, 70, 200), rect)
            pantalla.blit(texto, (rect.x + 10, rect.y + 5))
            pantalla.blit(valido, (rect.x + 200, rect.y + 5))
        pygame.display.flip()
        reloj.tick(FPS)

def playermenu(player, indexP, manager, players):
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    nombres_mazos = ["Seleccione mazo"]
    for (nombre, mazo, llave) in player.mazos:
        print(nombre)
        nombres_mazos.append(nombre)
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
    buscar_partida_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(508, 600, 350, 100),
        text='Buscar Partida',
        manager=manager
    )
    seleccion_mazo = pygame_gui.elements.UIDropDownMenu(
        options_list=nombres_mazos,
        starting_option=nombres_mazos[0],
        relative_rect=pygame.Rect((900, 600), (200, 50)),
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
            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == crearmazo:
                    manager.clear_and_reset()
                    players = nuevomazo(player.album, indexP, manager, players, max_seleccion=cantidad_cartas)
                    ejecutando = False
                    playermenu(player, indexP, manager, players)
                elif evento.ui_element == mazos:
                    manager.clear_and_reset()
                    vermazos(indexP, players)
                    ejecutando = False
                    playermenu(player, indexP, manager, players)
                elif evento.ui_element == buscar_partida_btn:
                    manager.clear_and_reset()
                    ejecutando = False
                    buscandomatch()
                    playermenu(player, indexP, manager, players)
            if evento.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == seleccion_mazo:
                    selected_option = evento.text  # Guardar el valor seleccionado
                    print(f"Opción seleccionada: {selected_option}")
            manager.process_events(evento)
        # Actualización y renderizado
        manager.update(tiempo_delta)
        pantalla.fill((0, 25, 50))  # Fondo azul oscuro
        manager.draw_ui(pantalla)

        pygame.display.flip()
    manager.clear_and_reset()

# Variable para controlar el mensaje de estado
mensaje = "Buscando partida..."  # Mensaje inicial
partida_encontrada = threading.Event()  # Evento para detectar cuando se encuentre la partida

def buscandomatch():
    global mensaje
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    reloj = pygame.time.Clock()
    ejecutando = True
    partida_encontrada = threading.Event()  # Crea un evento para el emparejamiento

    # Iniciar hilo de emparejamiento utilizando iniciar_emparejamiento
    hilo_emparejamiento = threading.Thread(target=iniciar_emparejamiento, args=(partida_encontrada,))
    hilo_emparejamiento.start()

    mostrar_mensaje = False
    ventana_mensaje = None

    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_WINDOW_CLOSE:
                    if evento.ui_element == ventana_mensaje:
                        ventana_mensaje = None
                        ejecutando = False  # Salimos del bucle cuando se cierra la ventana
            manager.process_events(evento)

        # Verifica si el emparejamiento ha finalizado
        if partida_encontrada.is_set() and not mostrar_mensaje:
            if getattr(partida_encontrada, 'result', False):
                mensaje = "Partida encontrada"
                # Aquí podrías iniciar la partida o realizar otras acciones
                ejecutando = False  # Salimos del bucle si se encontró partida
            else:
                mensaje = "No se encontraron oponentes"
                # Mostrar ventana de advertencia
                ventana_mensaje = mostrar_ventana_advertencia(manager, mensaje)
                mostrar_mensaje = True  # Para evitar mostrar múltiples mensajes

        manager.update(tiempo_delta)
        # Actualización y renderizado
        pantalla.fill((0, 25, 100))  # Fondo azul oscuro
        # Renderizar mensaje en pantalla
        font = pygame.font.Font(None, 36)
        texto = font.render("Buscando partida...", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO_VENTANA // 2 - texto.get_width() // 2, ALTO_VENTANA // 2))
        manager.draw_ui(pantalla)
        pygame.display.flip()