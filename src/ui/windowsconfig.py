import pygame
import pygame_gui

from src.managers.playerDataManager import load_players
from src.models.Album import Album
from src.managers import CardDataManager


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

# Inicializar jugadores cargados desde JSON
players = load_players()
if not players:
    players = []

cantidad_cartas = 5  # Configurable, cantidad de cartas iniciales