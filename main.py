import pygame
import pygame_gui

import random
import string

import ImageHandler
from Album import Album
from Carta import Carta
from CardDataManager import guardar_cartas_en_json, cargar_cartas_desde_json

pygame.init()

# Definimos algunas constantes
ANCHO_VENTANA = 1366
ALTO_VENTANA = 720
FPS = 60
CARTAS_CREADAS = []  # Lista para almacenar las cartas

# Cargar las cartas al inicio
CARTAS_CREADAS = cargar_cartas_desde_json()
album = Album()

def crear_ventana_crear_carta():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Crear Carta")

    manager = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA))

    # Texto para validaciones
    label_validacion_nombre = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 50), (500, 30)),
                                               text='Entre 5 y 30 caracteres',
                                               manager=manager,
                                                          )

    # Etiquetas de texto (Labels)
    label_nombre = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 20), (300, 30)),
                                               text='Nombre de la carta',
                                               manager=manager)
    label_descripcion = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 70), (300, 30)),
                                                    text='Descripción',
                                                    manager=manager)
    label_variante = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 120), (300, 30)),
                                                 text='Variante',
                                                 manager=manager)
    label_raza = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 170), (300, 30)),
                                             text='Nombre Variante',
                                             manager=manager)
    label_raza = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 220), (300, 30)),
                                                    text='Raza',
                                                    manager=manager)
    label_turno_poder = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 270), (300, 30)),
                                                    text='Turno de poder',
                                                    manager=manager)
    label_bonus_poder = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 320), (300, 30)),
                                                    text='Bonus de poder',
                                                    manager=manager)

    # Cuadros de entrada de texto
    entrada_nombre = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 50), (300, 30)), manager=manager)
    entrada_descripcion = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 100), (300, 30)), manager=manager)
    entrada_variante = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((50, 150), (300, 30)),
                                             starting_option="Si",
                                             options_list=["Si","No"],
                                             manager=manager)
    entrada_nombre_variante = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 200), (300, 30)),
                                                              manager=manager)
    entrada_raza = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((50, 250), (300, 30)),
                                             starting_option="Ogro",
                                             options_list=["Ogro","Elfo","Goblin"],
                                             manager=manager)
    entrada_turno_poder = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 300), (300, 30)), manager=manager)
    entrada_bonus_poder = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 350), (300, 30)), manager=manager)

    # Botones
    boton_crear = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 450), (150, 50)),
                                               text='Crear Carta',
                                               manager=manager)
    boton_imagen = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (150, 50)),
                                               text='Seleccionar imagen',
                                               manager=manager)

    # Variables para el bucle del juego
    reloj = pygame.time.Clock()
    ejecutando = True
    image_path = None

    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == entrada_variante:
                    valor_seleccionado_variante = evento.text
            if evento.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if evento.ui_element == entrada_raza:
                    valor_seleccionado_raza = evento.text
            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == boton_imagen:
                image_path = ImageHandler.open_file_dialog()  # Abrir el explorador de archivos

            if evento.type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == boton_crear:
                # Obtener los datos del formulario
                nombre_personaje = entrada_nombre.get_text()
                descripcion = entrada_descripcion.get_text()
                variante =valor_seleccionado_variante
                nombre_variante = entrada_nombre_variante.get_text()
                raza = valor_seleccionado_raza
                turno_poder = int(entrada_turno_poder.get_text())
                bonus_poder = int(entrada_bonus_poder.get_text())

                # Validaciones
                if ((len(nombre_personaje) >= 5 and len(nombre_personaje) <= 30)
                and len(descripcion) <= 1000):
                    nueva_carta = Carta(
                        nombre_personaje=nombre_personaje,
                        descripcion=descripcion,
                        nombre_variante=nombre_variante,
                        es_variante=variante,
                        selecRaza=raza,
                        raza=raza,
                        imagen=image_path,
                        tipo_carta="Normal",  # Tipo por defecto
                        turno_poder=turno_poder,
                        bonus_poder=bonus_poder,
                        atributos={'Poder': 50, 'Velocidad': 40}  # Valores predeterminados
                    )
                    #Volver a texto de validación inicial
                    label_validacion_nombre.set_text("Entre 5 y 30 caracteres")
                    #Guardar cartas
                    album.add(nueva_carta)
                    CARTAS_CREADAS.append(nueva_carta)
                    print(f"Carta creada: {nueva_carta}")
                    guardar_cartas_en_json(CARTAS_CREADAS)

                elif len(nombre_personaje) < 5 or len(nombre_personaje) > 30:
                    label_validacion_nombre.set_text("El nombre de la carta debe tener entre 5 y 30 caracteres intente de nuevo")



            manager.process_events(evento)

        manager.update(tiempo_delta)

        pantalla.fill((0, 0, 0))  # Fondo negro
        manager.draw_ui(pantalla)

        pygame.display.update()




# Función para mostrar el álbum de cartas con imágenes, con botón de alternar variantes
def mostrar_album(album):
    album.sorter()  # Ordenar cartas por nombre
    ANCHO_VENTANA = 800
    ALTO_VENTANA = 600
    FPS = 60
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
            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if not carta.es_variante]
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
                            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if not carta.es_variante]
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





# Programa principal
def main():
    album = Album()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Sistema de Gestión de Cartas")

    manager = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA))

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

if __name__ == '__main__':
    main()
