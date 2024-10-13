import pygame
import pygame_gui

import random
import string
from Carta import Carta
from Album import Album

pygame.init()

# Definimos algunas constantes
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60
CARTAS_CREADAS = []  # Lista para almacenar las cartas



def crear_ventana_crear_carta():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Crear Carta")

    manager = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA))

    # Widgets para ingresar los datos de la carta
    entrada_nombre = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 50), (300, 30)), manager=manager)
    entrada_descripcion = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 100), (300, 30)), manager=manager)
    entrada_variante = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 150), (300, 30)), manager=manager)
    entrada_raza = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 200), (300, 30)), manager=manager)
    entrada_turno_poder = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 250), (300, 30)), manager=manager)
    entrada_bonus_poder = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 300), (300, 30)), manager=manager)

    # Botón para crear la carta
    boton_crear = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (150, 50)),
                                               text='Crear Carta',
                                               manager=manager)

    # Variables para el bucle del juego
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        tiempo_delta = reloj.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == boton_crear:
                    # Obtener los datos del formulario
                    nombre_personaje = entrada_nombre.get_text()
                    descripcion = entrada_descripcion.get_text()
                    nombre_variante = entrada_variante.get_text()
                    raza = entrada_raza.get_text()
                    turno_poder = int(entrada_turno_poder.get_text())
                    bonus_poder = int(entrada_bonus_poder.get_text())

                    # Validaciones
                    if len(nombre_personaje) >= 5 and len(nombre_personaje) <= 30:
                        nueva_carta = Carta(
                            nombre_personaje=nombre_personaje,
                            descripcion=descripcion,
                            nombre_variante=nombre_variante,
                            raza=raza,
                            tipo_carta="Normal",  # Suponemos tipo carta normal por defecto
                            turno_poder=turno_poder,
                            bonus_poder=bonus_poder,
                            atributos={'Poder': 50, 'Velocidad': 40}  # Valores predeterminados
                        )

                        CARTAS_CREADAS.append(nueva_carta)
                        print(f"Carta creada: {nueva_carta}")

            manager.process_events(evento)

        manager.update(tiempo_delta)

        pantalla.fill((0, 0, 0))  # Fondo negro
        manager.draw_ui(pantalla)

        pygame.display.update()


# Función para mostrar el álbum de cartas con imágenes
def mostrar_album(album):
    ANCHO_VENTANA = 800
    ALTO_VENTANA = 600
    FPS = 60

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Álbum de Cartas")

    # Coordenadas para colocar el texto y las imágenes
    x_offset = 50
    y_offset = 50
    spacing = 150  # Espacio entre cartas

    # Calcula la altura total requerida para todas las cartas
    total_altura_cartas = len(album.obtener_cartas()) * spacing + y_offset

    # Tamaño del contenido visible en la ventana y el total que se puede desplazar
    contenido_visible = ALTO_VENTANA
    contenido_total = total_altura_cartas if total_altura_cartas > contenido_visible else contenido_visible

    # Inicializa la posición del scrollbar
    scroll_position = 0
    scroll_speed = 15  # Velocidad de desplazamiento con flechas
    scrollbar_altura = max(ALTO_VENTANA * (contenido_visible / contenido_total), 30)  # Tamaño mínimo de la barra
    scrollbar_pos_x = ANCHO_VENTANA - 20  # X para la barra de desplazamiento
    scrollbar_width = 15

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        tiempo_delta = reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            # Manejar el scroll del mouse solo para la barra
            if evento.type == pygame.MOUSEWHEEL:
                scroll_increment = -evento.y * album.size  
                scroll_position += scroll_increment

        # Fondo negro
        pantalla.fill((24, 0, 40))

        # Mostrar todas las cartas en el álbum
        for idx, carta in enumerate(album.obtener_cartas()):
            # Calcular la posición en función del valor de la barra de desplazamiento
            carta_pos = y_offset + (idx * spacing) - scroll_position

            # Mostrar la carta solo si está dentro de la ventana
            if carta_pos > -spacing and carta_pos < ALTO_VENTANA:
                # Cargar la imagen de la carta
                try:
                    imagen_carta = pygame.image.load(carta.image)
                    imagen_carta = pygame.transform.scale(imagen_carta, (100, 150))  # Redimensionar imagen
                    pantalla.blit(imagen_carta, (x_offset, carta_pos))
                except pygame.error as e:
                    print(f"Error al cargar la imagen {carta.imagen}: {e}")

                # Texto de la carta
                fuente = pygame.font.SysFont(None, 24)
                texto = fuente.render(f"{carta.nombre_personaje} - {carta.nombre_variante} - {carta.raza}", True,
                                      (255, 255, 255))
                pantalla.blit(texto, (x_offset + 120, carta_pos + 50))  # Alineación del texto al lado de la imagen

        # Dibuja el scrollbar
        scrollbar_pos_y = (scroll_position / (contenido_total - contenido_visible)) * (ALTO_VENTANA - scrollbar_altura)
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
