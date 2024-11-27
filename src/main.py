import pygame
import pygame_gui

from src.ui.playerwindows import mostrar_cardsforuser, addplayer, playermenu, newUser
from src.ui.Gwindows import mostrar_ventana_advertencia
from src.ui.adminwindows import admenu
from src.managers.playerDataManager import save_players, load_players
from src.ui.windowsconfig import ANCHO_VENTANA, ALTO_VENTANA, FPS, manager, CARTAS_CREADAS, album, players


pygame.init()


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
                newUser(False)
                begin()
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



def loguear():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    font = pygame.font.SysFont(None, 30)
    name = font.render("Alias o correo", True, (100, 100, 255))
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
                    if (player.alias == user or player.email == user) and player.password == password:
                        if player.esadmin == 0:
                            manager.clear_and_reset()
                            playermenu(player, i, manager, players)
                            ejecutando = False
                            begin()
                        else:
                            manager.clear_and_reset()
                            admenu()
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
    begin()
    pygame.quit()




if __name__ == '__main__':
    main()

