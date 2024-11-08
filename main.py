# main.py
import pygame
import pygame_gui
from Album import Album
import CardDataManager
from playerwindows import mostrar_cardsforuser, addplayer, playermenu
from Gwindows import mostrar_ventana_advertencia
from adminwindows import admenu
from playerDataManager import save_players, load_players  # Importar desde el nuevo módulo


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
                print(album.obtener_cartas())
                tempplayer = addplayer(entryname.get_text(), entryAlias.get_text(), country, entrycorreo.get_text(), entrycontra.get_text(), album)
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
                    save_players(players)
                    manager.clear_and_reset()
                    mostrar_cardsforuser(tempplayer[1][5], manager)
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
    entrycontra.set_text_hidden()
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
                i = 0
                for player in players:
                    i += 1
                    if user == "admin" and password == "admin":
                        manager.clear_and_reset()
                        admenu(manager, album, CARTAS_CREADAS)
                        ejecutando = False
                        begin()
                    if player[0] == user or player[4] == user and player[4] == password:
                        manager.clear_and_reset()
                        playermenu(player, i, manager, players)
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


#Programa principal
def main():
    pygame.display.set_caption("Sistema de Gestión de Cartas")
    #admenu(manager, album, CARTAS_CREADAS)
    begin()
    pygame.quit()




if __name__ == '__main__':
    main()
