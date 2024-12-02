import pygame
import pygame_gui

from src.managers.playerDataManager import save_players
from src.ui.windowsconfig import ANCHO_VENTANA, ALTO_VENTANA, FPS, manager, CARTAS_CREADAS, album, players



# Función para mostrar una ventana de advertencia con un mensaje personalizado
def mostrar_ventana_advertencia(manager, mensaje):
    ventana_advertencia = pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((500, 300), (300, 200)),
        html_message=f'<b>{mensaje}</b>',
        manager=manager,
        window_title="Advertencia"
    )
    return ventana_advertencia  # Ahora devuelve el objeto de la ventana

# Función para mostrar una ventana de confirmación de éxito
def mostrar_ventana_listo(manager):
    ventana_advertencia = pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((500, 300), (300, 200)),  # Tamaño y posición de la ventana
        html_message=f'<b>{"Carta creada con exito"}</b>',
        manager=manager,
        window_title="Listo"
    )

# Función para mostrar el álbum de cartas con imágenes, con botón de alternar variantes
def mostrar_album(albumm):
    albumm.sorter()  # Ordenar cartas por nombre
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
        cartas_a_mostrar = albumm.obtener_cartas()
        if not mostrar_variantes:
            cartas_a_mostrar = [carta for carta in cartas_a_mostrar if carta.es_variante == "No"]
    except Exception as e:
        error_carga = True
        cartas_a_mostrar = []

#Calcular dimensiones para scroll y scrollbar
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
                        cartas_a_mostrar = albumm.obtener_cartas()
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

