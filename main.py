import pygame
import pygame_gui
import ImageHandler
import random
from Album import Album, playerAlbum
from Carta import Carta
import CardDataManager
from Cardlogic import svariant, isvalid, getatr
import re

pygame.init()

# Definimos algunas constantes
ANCHO_VENTANA = 1366
ALTO_VENTANA = 720
FPS = 60





#Manager
manager = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA))

# Cargar las cartas al inicio
CARTAS_CREADAS = CardDataManager.cargar_cartas_desde_json()
album = Album()
players = [["Hardok", "Hardok", "Costa Rica", "Hardok", "Hardok", album, [("Principal", album)]]]

def crear_atributos(manager):
    atributos = ['Poder', 'Velocidad', 'Magia', 'Defensa', 'Inteligencia', 'Altura',
                 'Fuerza', 'Agilidad', 'Salto', 'Resistencia', 'Flexibilidad',
                 'Explosividad', 'Carisma', 'Habilidad', 'Balance', 'Sabiduría',
                 'Suerte', 'Coordinación', 'Amabilidad', 'Lealtad', 'Disciplina',
                 'Liderazgo', 'Prudencia', 'Confianza', 'Percepción', 'Valentía']

    num_atributos = len(atributos)
    mitad = num_atributos // 2
    atributo_entries = []

    # Primera mitad
    for i in range(mitad):
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((400, 20 + i * 40), (200, 30)),
                                    text=atributos[i],
                                    manager=manager)
        entrada_atributo = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, 20 + i * 40), (100, 30)),
                                                               manager=manager)
        if entrada_atributo == "":
            atributo_entries.append(0)
            continue
        atributo_entries.append(entrada_atributo)

    # Segunda mitad (más a la derecha)
    for i in range(mitad, num_atributos):
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((800, 20 + (i - mitad) * 40), (200, 30)),
                                    text=atributos[i],
                                    manager=manager)
        entrada_atributo = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((1000, 20 + (i - mitad) * 40), (100, 30)),
            manager=manager)
        if entrada_atributo == "":
            atributo_entries.append(0)
            continue
        atributo_entries.append(entrada_atributo)

    return atributo_entries, atributos

def mostrar_ventana_advertencia(manager, mensaje):
    ventana_advertencia = pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((500, 300), (300, 200)),  # Tamaño y posición de la ventana
        html_message=f'<b>{mensaje}</b>',
        manager=manager,
        window_title="Advertencia"
)

def mostrar_ventana_listo(manager):
    ventana_advertencia = pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((500, 300), (300, 200)),  # Tamaño y posición de la ventana
        html_message=f'<b>{"Carta creada con exito"}</b>',
        manager=manager,
        window_title="Listo"
    )

def crear_ventana_crear_carta():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Crear Carta")

    # Etiquetas de texto (Labels)
    label_nombre = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 20), (300, 30)),
                                               text='Nombre de la carta',
                                               manager=manager)
    label_descripcion = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 70), (300, 30)),
                                                    text='Descripción',
                                                    manager=manager)

    label_nombre_variante = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 120), (300, 30)),
                                                        text='Nombre Variante',
                                                        manager=manager)

    label_raza = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 170), (300, 30)),
                                             text='Raza',
                                             manager=manager)
    label_turno_poder = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 220), (300, 30)),
                                                    text='Turno de poder',
                                                    manager=manager)
    label_bonus_poder = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 270), (300, 30)),
                                                    text='Bonus de poder',
                                                    manager=manager)
    label_tipo_carta = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 320), (300, 30)),
                                                    text='Tipo de carta',
                                                    manager=manager)

    # Cuadros de entrada de texto
    entrada_nombre = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 50), (300, 30)),
                                                         manager=manager)
    entrada_descripcion = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 100), (300, 30)),
                                                              manager=manager)

    entrada_nombre_variante = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 150), (300, 30)),
                                                                  manager=manager)
    entrada_raza = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((50, 200), (300, 30)),
                                                      starting_option="Ogro",
                                                      options_list=["Ogro", "Elfo", "Goblin"],
                                                      manager=manager)
    entrada_turno_poder = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 250), (300, 30)),
                                                              manager=manager)
    entrada_bonus_poder = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 300), (300, 30)),
                                                              manager=manager)
    entrada_tipo_carta = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((50, 350), (300, 30)),
                                                      starting_option="Básica",
                                                      options_list=["Ultra-Rara","Muy Rara", "Rara", "Normal","Básica"],
                                                      manager=manager)

    # Crear atributos y obtener sus entradas
    atributo_entries, atributos = crear_atributos(manager)

    # Botones
    boton_crear = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 500), (150, 50)),
                                               text='Crear Carta',
                                               manager=manager)
    boton_imagen = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 450), (150, 50)),
                                                text='Seleccionar imagen',
                                                manager=manager)

    # Variables para el bucle del juego
    reloj = pygame.time.Clock()
    ejecutando = True
    image_path = None
    valor_seleccionado_variante = 1



    while ejecutando:

        tiempo_delta = reloj.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == entrada_raza:
                    valor_seleccionado_raza = evento.text
            if evento.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == entrada_tipo_carta:
                    valor_seleccionado_tipo = evento.text
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == boton_imagen:
                image_path = ImageHandler.open_file_dialog()  # Abrir el explorador de archivos

            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == boton_crear:
                # Obtener los datos del formulario
                nombre_personaje = entrada_nombre.get_text()
                descripcion = entrada_descripcion.get_text()
                nombre_variante = entrada_nombre_variante.get_text()



                #define turno_poder y bonus_poder
                turno_poder = -1
                if entrada_turno_poder.get_text().isnumeric(): turno_poder = int(entrada_turno_poder.get_text())
                bonus_poder = -1
                if entrada_bonus_poder.get_text().isnumeric(): bonus_poder = int(entrada_bonus_poder.get_text())

                try:
                    raza = valor_seleccionado_raza
                except:
                    raza = "Ogro"


                #define el tipo de carta
                try:
                    tipo_carta = valor_seleccionado_tipo
                except:
                    tipo_carta = "Basica"




                # Recoger los atributos ingresados
                atributos_ingresados = getatr(atributo_entries, atributos)



                # Valida si todos las entradas están correctas
                valid = isvalid(manager, atributo_entries, nombre_personaje, descripcion, turno_poder, bonus_poder)
                if not valid[0]:
                    mostrar_ventana_advertencia(manager, valid[1])
                    continue



                nueva_carta = Carta(
                    nombre_personaje=nombre_personaje,
                    descripcion=descripcion,
                    nombre_variante=nombre_variante,
                    selecRaza=raza,
                    es_variante= svariant(nombre_personaje),
                    raza=raza,
                    imagen=image_path,
                    tipo_carta=tipo_carta,
                    turno_poder=turno_poder,
                    bonus_poder=bonus_poder,
                    atributos=atributos_ingresados  # Asignar atributos ingresados
                )

                #Guardar cartas
                CARTAS_CREADAS.append(nueva_carta)
                print(f"Carta creada: {nueva_carta}")
                CardDataManager.guardar_cartas_en_json(CARTAS_CREADAS)

                #Mostar ventana para notificar el exito en la creacion
                mostrar_ventana_listo(manager)

                ejecutando = False
                crear_ventana_crear_carta()


            manager.process_events(evento)

        manager.update(tiempo_delta)

        pantalla.fill((0, 0, 0))  # Fondo negro
        manager.draw_ui(pantalla)

        pygame.display.update()

# Función para mostrar el álbum de cartas con imágenes, con botón de alternar variantes
def mostrar_album(album):
    album.clean()
    album.getcartascreadas()
    album.sorter()  # Ordenar cartas por nombre
    mostrar_variantes = True  # Inicialmente no mostrar variantes

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Álbum de Cartas")

    # Coordenadas para colocar el texto y las imágenes
    x_offset = 50
    y_offset = 50
    imagen_ancho = 100
    imagen_alto = 150
    texto_espacio_vertical = 30  # Espacio vertical entre líneas de texto
    carta_espacio_vertical = imagen_alto + 120  # Espacio vertical entre cartas

    # Definir área del botón (X, Y, Ancho, Alto)
    boton_rect = pygame.Rect(ANCHO_VENTANA - 150, 10, 130, 40)

    reloj = pygame.time.Clock()
    ejecutando = True
    error_carga = False
    scroll_position = 0
    scroll_speed = 15  # Velocidad de desplazamiento

    # Obtener las cartas al principio
    try:
        cartas_a_mostrar = album.obtener_cartas()
        if not mostrar_variantes:
            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if carta.es_variante == "No"]
    except Exception as e:
        error_carga = True
        cartas_a_mostrar = []

    # Calcula la altura total requerida para todas las cartas
    total_altura_cartas = len(cartas_a_mostrar) * carta_espacio_vertical + y_offset

    # Tamaño del contenido visible en la ventana y el total que se puede desplazar
    contenido_visible = ALTO_VENTANA
    contenido_total = total_altura_cartas if total_altura_cartas > contenido_visible else contenido_visible

    # Tamaño del scrollbar
    scrollbar_altura = max(ALTO_VENTANA * (contenido_visible / contenido_total), 30)  # Tamaño mínimo de la barra
    scrollbar_pos_x = ANCHO_VENTANA - 20
    scrollbar_width = 15

    while ejecutando:
        tiempo_delta = reloj.tick(FPS)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            # Detectar clics del mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):  # Si el clic está en el área del botón
                    mostrar_variantes = not mostrar_variantes  # Alternar el estado de mostrar_variantes
                    # Actualizar las cartas a mostrar según el estado del botón
                    try:
                        cartas_a_mostrar = album.obtener_cartas()
                        if not mostrar_variantes:
                            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if carta.es_variante == "No"]
                    except Exception as e:
                        error_carga = True
                        cartas_a_mostrar = []
                    # Recalcular la altura total de las cartas
                    total_altura_cartas = len(cartas_a_mostrar) * carta_espacio_vertical + y_offset
                    contenido_total = total_altura_cartas if total_altura_cartas > contenido_visible else contenido_visible
                    scrollbar_altura = max(ALTO_VENTANA * (contenido_visible / contenido_total), 30)

            # Manejar el scroll del mouse
            if evento.type == pygame.MOUSEWHEEL:
                scroll_increment = -evento.y * scroll_speed
                scroll_position = max(0, min(scroll_position + scroll_increment, contenido_total - contenido_visible))

        # Fondo negro
        pantalla.fill((24, 0, 40))

        # Dibujar el botón
        pygame.draw.rect(pantalla, (0, 255, 0), boton_rect)  # Rectángulo verde
        fuente = pygame.font.SysFont(None, 24)
        boton_texto = "Ver Variantes" if not mostrar_variantes else "Ocultar Variantes"
        pantalla.blit(fuente.render(boton_texto, True, (0, 0, 0)), (boton_rect.x + 10, boton_rect.y + 10))

        if error_carga:
            # Mostrar mensaje de error si hay problemas al cargar las cartas
            pantalla.blit(fuente.render("Error al cargar cartas, intente más tarde.", True, (255, 0, 0)),
                          (x_offset, ALTO_VENTANA // 2))
        elif not cartas_a_mostrar:
            # Mostrar mensaje si no hay cartas en el álbum
            pantalla.blit(fuente.render("No existen cartas creadas.", True, (255, 255, 255)),
                          (x_offset, ALTO_VENTANA // 2))
        else:
            # Mostrar las cartas en el álbum
            for idx, carta in enumerate(cartas_a_mostrar):
                carta_pos = y_offset + (idx * carta_espacio_vertical) - scroll_position

                if carta_pos > -carta_espacio_vertical and carta_pos < ALTO_VENTANA:
                    try:
                        imagen_carta = pygame.image.load(carta.imagen)
                        imagen_carta = pygame.transform.scale(imagen_carta, (imagen_ancho, imagen_alto))
                        pantalla.blit(imagen_carta, (x_offset, carta_pos))
                    except pygame.error as e:
                        print(f"Error al cargar la imagen {carta.imagen}: {e}")

                    # Mostrar los textos alineados con más espaciado
                    texto = f"Personaje: {carta.nombre_personaje}"
                    variante = f"Variante: {carta.nombre_variante}" if carta.nombre_variante else "Sin variante"
                    raza = f"Raza: {carta.raza}"
                    tipo_carta = f"Tipo de carta: {carta.tipo_carta}"
                    estado_juego = f"En juego: {'Activa' if carta.activa_en_juego else 'Inactiva'}"
                    estado_sobres = f"En sobres: {'Activa' if carta.activa_en_sobres else 'Inactiva'}"
                    llave = f"Llave única: {carta.llave_identificadora}"
                    fecha_modificacion = f"Fecha mod: {carta.fecha_modificacion}"

                    pantalla.blit(fuente.render(texto, True, (255, 255, 255)), (x_offset + imagen_ancho + 20, carta_pos))
                    pantalla.blit(fuente.render(variante, True, (255, 255, 255)),
                                  (x_offset + imagen_ancho + 20, carta_pos + texto_espacio_vertical))
                    pantalla.blit(fuente.render(raza, True, (255, 255, 255)),
                                  (x_offset + imagen_ancho + 20, carta_pos + 2 * texto_espacio_vertical))
                    pantalla.blit(fuente.render(tipo_carta, True, (255, 255, 255)),
                                  (x_offset + imagen_ancho + 20, carta_pos + 3 * texto_espacio_vertical))
                    pantalla.blit(fuente.render(estado_juego, True, (255, 255, 255)),
                                  (x_offset + imagen_ancho + 20, carta_pos + 4 * texto_espacio_vertical))
                    pantalla.blit(fuente.render(estado_sobres, True, (255, 255, 255)),
                                  (x_offset + imagen_ancho + 20, carta_pos + 5 * texto_espacio_vertical))
                    pantalla.blit(fuente.render(llave, True, (255, 255, 255)),
                                  (x_offset + imagen_ancho + 20, carta_pos + 6 * texto_espacio_vertical))
                    pantalla.blit(fuente.render(fecha_modificacion, True, (255, 255, 255)),
                                  (x_offset + imagen_ancho + 20, carta_pos + 7 * texto_espacio_vertical))

        # Dibuja el scrollbar
        scrollbar_pos_y = (scroll_position / (contenido_total - contenido_visible + 1)) * (
                    ALTO_VENTANA - scrollbar_altura)
        pygame.draw.rect(pantalla, (200, 200, 200),
                         (scrollbar_pos_x, scrollbar_pos_y, scrollbar_width, scrollbar_altura))

        pygame.display.update()

def admenu():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    # Botones para las diferentes funcionalidades
    boton_crear_carta = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (200, 50)),
                                                     text='Crear Carta',
                                                     manager=manager)

    boton_ver_album = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (200, 50)),
                                                   text='Ver Álbum',
                                                   manager=manager)

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == boton_crear_carta:
                    crear_ventana_crear_carta()
                elif evento.ui_element == boton_ver_album:
                    mostrar_album(album)

            manager.process_events(evento)

        manager.update(tiempo_delta)

        pantalla.fill((0,25, 50))  # Fondo negro
        manager.draw_ui(pantalla)

        pygame.display.update()

def playermenu(player):
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

    vermazos = pygame_gui.elements.UIButton(
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

        # Event handling
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == crearmazo:
                manager.clear_and_reset()
                nuevomazo(player[5], max_seleccion=4)
                ejecutando = False
                playermenu(player)

            manager.process_events(evento)




        # Update and render elements
        manager.update(tiempo_delta)
        pantalla.fill((0, 25, 50))  # Dark blue background
        manager.draw_ui(pantalla)

        pygame.display.flip()
    manager.clear_and_reset()

def begin():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    font = pygame.font.SysFont(None, 50)
    text = font.render("Bienvenido a PowerDeck", True, (100, 100, 255))
    posi = [pantalla.get_rect().centerx, pantalla.get_rect().centery - 300]

    # Crear botones
    registrarse = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (ANCHO_VENTANA - 200) / 2,
            ALTO_VENTANA - 320,
            200, 60
        ),
        text='Registrarse',
        manager=manager
    )
    login = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (ANCHO_VENTANA - 200) / 2,
            ALTO_VENTANA - 450,
            200, 60
        ),
        text='Login',
        manager=manager
    )

    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == registrarse:
                registrarse.kill()  # Elimina el botón "Registrarse"
                login.kill()  # Elimina el botón "Login"
                ejecutando = False  # Salimos del bucle para terminar "begin"
                newUser()
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == login:
                registrarse.kill()  # Elimina el botón "Registrarse"
                login.kill()  # Elimina el botón "Login"
                ejecutando = False  # Salimos del bucle para terminar "begin"
                loguear()

            manager.process_events(evento)
        manager.update(tiempo_delta)
        pantalla.fill((0, 25, 50))
        pantalla.blit(text, text.get_rect(center=posi))
        manager.draw_ui(pantalla)
        pygame.display.flip()

def newUser():
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
                                                      options_list=["", "Argentina", "Perú", "Uruguay", "México", "Costa Rica", "Bolivia", ],
                                                      manager=manager)

    entrycorreo = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((798, 110), (300, 30)),
                                                         manager=manager)

    entrycontra = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((798, 310), (300, 30)),
                                                         manager=manager)

    registrarse = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(825, 550, 250, 50),
        text='Registrarse',
        manager=manager
    )
    country = ""


    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        puedeasignar = True
        tiempo_delta = reloj.tick(FPS) / 1000.0

        # Event handling
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == paisentry:
                    country = evento.text

            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == registrarse:
                tempplayer = addplayer(entryname.get_text(), entryAlias.get_text(), country, entrycorreo.get_text(), entrycontra.get_text())
                if not tempplayer[0]:
                    mostrar_ventana_advertencia(manager, tempplayer[2])
                    continue

                for player in players:
                    if player[0] == entryname.get_text() or player[3] == entrycorreo.get_text():
                        puedeasignar = False
                        mostrar_ventana_advertencia(manager, "El correo o el nombre ya existe")
                        tempplayer = []
                        break


                if puedeasignar:
                    players.append(tempplayer[1])
                    manager.clear_and_reset()
                    mostrar_cardsforuser(tempplayer[1][5])
                    ejecutando = False



            manager.process_events(evento)



        # Update and render elements
        manager.update(tiempo_delta)
        pantalla.fill((0, 25, 50))  # Dark blue background
        pantalla.blit(name, name.get_rect(topleft=(70, 70)))
        pantalla.blit(Alias, Alias.get_rect(topleft=(70, 270)))
        pantalla.blit(pais, pais.get_rect(topleft=(70, 470)))
        pantalla.blit(correo, correo.get_rect(topleft=(800, 70)))
        pantalla.blit(contra, contra.get_rect(topleft=(800, 270)))

        manager.draw_ui(pantalla)

        pygame.display.flip()
    manager.clear_and_reset()
    begin()

def loguear():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    font = pygame.font.SysFont(None, 30)
    name = font.render("Nombre de usuario o correo", True, (100, 100, 255))
    contra = font.render("Contraseña", True, (100, 100, 255))
    entryname = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((533, 250), (300, 30)),
                                                         manager=manager)

    entrycontra = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((533, 400), (300, 30)),
                                                         manager=manager)
    Login = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(558, 500, 250, 50),
        text='Login',
        manager=manager
    )

    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        # Event handling
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                manager.clear_and_reset()
                begin()
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == Login:
                if entrycontra.get_text() == "" or entryname.get_text() == "":
                    mostrar_ventana_advertencia(manager, "Debe completar ambas entradas")
                    continue
                password = entrycontra.get_text()
                user = entryname.get_text()
                for player in players:
                    if player[0] == user or player[4] == user and player[4] == password:
                        manager.clear_and_reset()
                        playermenu(player)
                        ejecutando = False
                        begin()
                mostrar_ventana_advertencia(manager, "Información incorrecta")
            manager.process_events(evento)


        # Update and render elements
        manager.update(tiempo_delta)
        pantalla.fill((0, 25, 50))  # Dark blue background
        pantalla.blit(name, name.get_rect(center=[pantalla.get_rect().centerx, pantalla.get_rect().centery - 150]))
        pantalla.blit(contra, contra.get_rect(center=[pantalla.get_rect().centerx, pantalla.get_rect().centery]))
        manager.draw_ui(pantalla)

        pygame.display.flip()

    manager.clear_and_reset()

def addplayer(name, alias, pais, correo, contra):
    mensaje = ""
    i = 0
    result = True

    patron = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'

    if pais == "":
        mensaje = "Debe seleccionar su país"
        i = 5
        result = False
    if correo == "" or contra == "":
        mensaje = "Se deben llenar todos los campos requeridos"
        i = 5
        result = False

    if not len(name) in range(4, 12) or not len(alias) in range(4, 12):
        mensaje = "El nombre y alias deben estar entre 4 y 12 carácteres"
        i = 5
        result = False
    if not re.match(patron, correo):
        mensaje = "Inserte un email válido"
        i = 5
        result = False

    albumplayer = playerAlbum()
    mazos = []


    yaregistrados = []
    while i < 4:
        continuar = True
        o = random.randint(1, album.size)
        if album.getcard(o).es_variante == "Si":
            yaregistrados.append(o)
            continuar = False
        for l in yaregistrados:
            if o == l:
                continuar = False
                break
        if continuar:
            i += 1
            yaregistrados.append(o)
            albumplayer.add(album.getcard(o))

    print(albumplayer.obtener_cartas())
    return result, [name, alias, pais, correo, contra, albumplayer, mazos], mensaje

def mostrar_cardsforuser(playeralbum):
    pantalla = pygame.display.set_mode((1000, 600))
    font = pygame.font.SysFont(None, 20)
    font2 = pygame.font.SysFont(None, 35)
    asignadas = font2.render("Se te han asignado estas 4 cartas", True, (100, 100, 255))

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

        # Event handling
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == continuar:
                ejecutando = False
            manager.process_events(evento)

        pantalla.fill((0, 25, 0))  # Fill screen at the start of each frame

        cartax = 200

        # Display the cards
        for i in range(1, 5):
            carta = playeralbum.getcard(i)
            try:
                imagen_carta = pygame.image.load(carta.imagen)
                imagen_carta = pygame.transform.scale(imagen_carta, (imagen_ancho, imagen_alto))
                pantalla.blit(imagen_carta, (cartax, 200))
                pantalla.blit(font.render(carta.nombre_personaje, True, (100, 100, 255)), (cartax, 350))
                cartax += 175
            except pygame.error as e:
                print(f"Error al cargar la imagen {carta.imagen}: {e}")
        pantalla.blit(asignadas, asignadas.get_rect(center=[pantalla.get_rect().centerx, pantalla.get_rect().centery - 180]))
        # Update and render elements
        manager.update(tiempo_delta)
        manager.draw_ui(pantalla)
        pygame.display.flip()

# Función para mostrar el álbum de cartas con imágenes, con botón de alternar variantes y selección múltiple
def nuevomazo(playeralbum, max_seleccion=4):
    print(playeralbum.obtener_cartas(), "AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    playeralbum.sorter()  # Ordenar cartas por nombre
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

    # Coordenadas y dimensiones
    x_offset = 50
    y_offset = 50
    imagen_ancho = 100
    imagen_alto = 150
    texto_espacio_vertical = 30
    carta_espacio_vertical = imagen_alto + 120

    # Definir botón de alternar variantes
    boton_rect = pygame.Rect(ANCHO_VENTANA - 150, 10, 130, 40)
    reloj = pygame.time.Clock()
    ejecutando = True
    scroll_position = 0
    scroll_speed = 30



    # Obtener cartas y preprocesar para mostrar
    try:
        cartas_a_mostrar = playeralbum.obtener_cartas()
        if not mostrar_variantes:
            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if carta.es_variante == "No" or  carta.es_variante == False]
    except Exception as e:
        print("Error al cargar cartas:", e)
        cartas_a_mostrar = []

    # Control de selección de cartas
    cartas_seleccionadas = []

    # Calcular altura total de cartas para scroll
    total_altura_cartas = len(cartas_a_mostrar) * carta_espacio_vertical + y_offset
    contenido_visible = ALTO_VENTANA
    contenido_total = total_altura_cartas if total_altura_cartas > contenido_visible else contenido_visible

    # Tamaño del scrollbar
    scrollbar_altura = max(ALTO_VENTANA * (contenido_visible / contenido_total), 30)
    scrollbar_pos_x = ANCHO_VENTANA - 20
    scrollbar_width = 15

    while ejecutando:
        tiempo_delta = reloj.tick(FPS)

        # Eventos
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
                            cartas_seleccionadas.remove(carta)  # Deseleccionar
                        elif len(cartas_seleccionadas) < max_seleccion:
                            cartas_seleccionadas.append(carta)  # Seleccionar
                        break

            # Scroll con rueda del mouse
            if evento.type == pygame.MOUSEWHEEL:
                scroll_increment = -evento.y * scroll_speed
                scroll_position = max(0, min(scroll_position + scroll_increment, contenido_total - contenido_visible))
            manager.process_events(evento)
        # Fondo de la pantalla
        pantalla.fill((24, 0, 40))

        # Botón de alternar variantes
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
                    # Mostrar borde de selección
                    if carta in cartas_seleccionadas:
                        pygame.draw.rect(pantalla, (255, 0, 0),
                                         pygame.Rect(x_offset, carta_pos, imagen_ancho, imagen_alto), 3)
                except pygame.error as e:
                    print(f"Error al cargar la imagen {carta.imagen}: {e}")

                # Textos de carta
                pantalla.blit(fuente.render(f"Personaje: {carta.nombre_personaje}", True, (255, 255, 255)),
                              (x_offset + imagen_ancho + 20, carta_pos))


        # Scrollbar
        scrollbar_pos_y = (scroll_position / (contenido_total - contenido_visible + 1)) * (
                    ALTO_VENTANA - scrollbar_altura)
        pygame.draw.rect(pantalla, (200, 200, 200),
                         (scrollbar_pos_x, scrollbar_pos_y, scrollbar_width, scrollbar_altura))

        manager.update(tiempo_delta)
        manager.draw_ui(pantalla)
        pygame.display.update()
    manager.clear_and_reset()
    return cartas_seleccionadas

#Programa principal
def main():
    pygame.display.set_caption("Sistema de Gestión de Cartas")
    begin()
    pygame.quit()




if __name__ == '__main__':
    main()
