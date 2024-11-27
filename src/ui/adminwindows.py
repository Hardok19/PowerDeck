import pygame
import pygame_gui
from src.managers import CardDataManager
from src.models.Carta import Carta
from src.logic.Cardlogic import svariant, isvalid, getatr
from src.ui.Gwindows import mostrar_ventana_advertencia, mostrar_ventana_listo, mostrar_album
from src.utils import ImageHandler
from src.ui.windowsconfig import ANCHO_VENTANA, ALTO_VENTANA, FPS, manager, CARTAS_CREADAS, album
from src.ui.playerwindows import newUser
from src.matchmaking.server import start_server, stop
import threading


HILO4server = 1

# Función para crear las entradas de atributos en la interfaz de usuario
def crear_atributos():
    atributos = ['Poder', 'Velocidad', 'Magia', 'Defensa', 'Inteligencia', 'Altura',
                 'Fuerza', 'Agilidad', 'Salto', 'Resistencia', 'Flexibilidad',
                 'Explosividad', 'Carisma', 'Habilidad', 'Balance', 'Sabiduría',
                 'Suerte', 'Coordinación', 'Amabilidad', 'Lealtad', 'Disciplina',
                 'Liderazgo', 'Prudencia', 'Confianza', 'Percepción', 'Valentía']

    num_atributos = len(atributos)
    mitad = num_atributos // 2
    atributo_entries = []

    # Primera mitad de los atributos en la columna izquierda
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
    # Segunda mitad de los atributos en la columna derecha
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
# Función para crear la ventana de creación de cartas
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
    atributo_entries, atributos = crear_atributos()

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
                manager.clear_and_reset()
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

#Función para el menú de administración
def admenu():
    global HILO4server
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    # Botones para las diferentes funcionalidades
    boton_crear_carta = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (200, 50)),
                                                     text='Crear Carta',
                                                     manager=manager)

    boton_ver_album = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (200, 50)),
                                                   text='Ver Álbum',
                                                   manager=manager)
    boton_crear_admin = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 250), (200, 50)),
                                                   text='Crear Admin',
                                                   manager=manager)
    boton_matchmaking = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 350), (200, 50)),
                                                   text='Start matchmaking',
                                                   manager=manager)

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if HILO4server.is_alive():
                    stop()
                ejecutando = False
                manager.clear_and_reset()
            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == boton_crear_carta:
                    manager.clear_and_reset()
                    crear_ventana_crear_carta()
                    ejecutando = False
                    admenu()
                elif evento.ui_element == boton_ver_album:
                    album.clean()
                    album.getcartascreadas()
                    mostrar_album(album)
                elif evento.ui_element == boton_crear_admin:
                    manager.clear_and_reset()
                    newUser(True)
                    ejecutando = False
                    admenu()
                elif evento.ui_element == boton_matchmaking:
                    HILO4server = threading.Thread(target=start_server, args=(5555,))
                    HILO4server.start()
                    boton_matchmaking.kill()
                    mostrar_ventana_advertencia(manager, "Server de matchmaking iniciado")

            manager.process_events(evento)

        manager.update(tiempo_delta)
        pantalla.fill((0,25, 50))  # Fondo negro
        manager.draw_ui(pantalla)
        pygame.display.update()


