import re
from src.models.player import player
from src.logic.Cardlogic import generarcartas
from src.models.Album import playerAlbum

def validate_player_data(name, alias, pais, correo, contra, isadmin):
    mensaje = ""
    result = True
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'

    # Validaciones de entrada
    if pais == "":
        mensaje = "Debe seleccionar su país"
        result = False
    elif correo == "" or contra == "":
        mensaje = "Se deben llenar todos los campos requeridos"
        result = False
    elif not len(alias) in range(4, 12):
        mensaje = "El alias debe tener entre 4 y 12 caracteres"
        result = False
    elif not re.match(email_pattern, correo):
        mensaje = "Inserte un email válido"
        result = False
    elif not re.match(password_pattern, contra):
        mensaje = ("La contraseña debe ser alfanumérica, contener al menos una letra, "
                   "un número y tener mínimo 6 caracteres")
        result = False

    return result, mensaje

def create_player(name, alias, pais, correo, contra, album, isadmin, cantidad_cartas):
    # Asignación de cartas iniciales
    cartas_iniciales = generarcartas(album, cantidad_cartas)
    albumplayer = playerAlbum(0)
    if not isadmin:
        # Agregar las cartas iniciales al álbum del jugador
        for carta in cartas_iniciales:
            albumplayer.add(carta)
    mazos = []
    grado = 1 if isadmin else 0  # Grado de permisos, 1 para admin, 0 para jugador
    TEMPplayer = player(name, alias, pais, correo, contra, "", grado, albumplayer, mazos)
    return TEMPplayer

def create_new_deck(playeralbum, selected_cards, deck_name, existing_decks, max_cards):
    mensaje = ""
    if len(selected_cards) != max_cards:
        mensaje = f"Debe seleccionar exactamente {max_cards} cartas."
        return False, mensaje

    for mazo in existing_decks:
        if mazo[0] == deck_name:
            mensaje = "Un mazo con ese nombre ya existe en tus mazos."
            return False, mensaje

    if deck_name == "":
        mensaje = "Ingrese un nombre para el mazo."
        return False, mensaje

    # Crear el nuevo mazo
    temp_album = playerAlbum(1)
    for card in selected_cards:
        temp_album.add(card)
    return True, temp_album

def validate_admin_data(name, correo, contra, admin_type):
    mensaje = ""
    result = True
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
    if not admin_type in ["Administrador de Control", "Administrador de Juego"]:
        mensaje = "Tipo de administrador inválido"
        result = False
    elif correo == "" or contra == "":
        mensaje = "Se deben llenar todos los campos requeridos"
        result = False
    elif not re.match(email_pattern, correo):
        mensaje = "Inserte un email válido"
        result = False
    elif not re.match(password_pattern, contra):
        mensaje = ("La contraseña debe ser alfanumérica, contener al menos una letra, "
                   "un número y tener mínimo 6 caracteres")
        result = False
    return result, mensaje

def create_admin(name, correo, contra, admin_type):
    # Grado de permisos: 1 para Administrador de Control, 2 para Administrador de Juego
    if admin_type == "Administrador de Control":
        grado = 1
    else:
        grado = 2
    albumplayer = playerAlbum(0)
    mazos = []
    TEMPadmin = player(name, "", "", correo, contra, "", grado, albumplayer, mazos)
    return TEMPadmin

def start_matchmaking(partida_encontrada):
    # Aquí iría la lógica para iniciar el emparejamiento
    pass