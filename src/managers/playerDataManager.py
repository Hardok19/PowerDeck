import json
from src.models.Album import playerAlbum
from src.models.player import player as player111



filename = '../data/players.json'

def player_to_dict(player):
    print({
        'name': player.name,
        'alias': player.alias,
        'country': player.country,
        'email': player.email,
        'password': player.password,
        "llave": player.llave,
        "esadmin": player.esadmin,
        'album': player.album.to_list(),
        'mazos': [{'nombre': nombre_mazo, 'album': mazo_album.to_list(), "llave": llave} for nombre_mazo, mazo_album, llave in player.mazos]
    })
    return {
        'name': player.name,
        'alias': player.alias,
        'country': player.country,
        'email': player.email,
        'password': player.password,
        "llave": player.llave,
        "esadmin": player.esadmin,
        'album': player.album.to_list(),
        'mazos': [{'nombre': nombre_mazo, 'album': mazo_album.to_list(), "llave": llave} for nombre_mazo, mazo_album, llave in player.mazos]
    }

def player_from_dict(data):
    name = data['name']
    alias = data['alias']
    country = data['country']
    email = data['email']
    password = data['password']
    llave = data["llave"]
    esadmin = data["esadmin"]
    album = playerAlbum(0).from_list(data['album'], 0)
    mazos = [(mazo_data['nombre'], playerAlbum.from_list(mazo_data['album'], 1), mazo_data["llave"]) for mazo_data in data['mazos']]
    temppla = player111(name, alias, country, email, password, llave, esadmin, album, mazos)
    return temppla

def save_players(players):
    players_data = [player_to_dict(player) for player in players]
    try:
        with open(filename, 'w') as f:
            json.dump(players_data, f, indent=4)
        print("Jugadores guardados exitosamente en players.json")
    except Exception as e:
        print("Error al guardar jugadores:", e)

def load_players():
    try:
        with open(filename, 'r') as f:
            content = f.read()
            if not content.strip():
                # El archivo está vacío
                return []
            players_data = json.loads(content)
        return [player_from_dict(data) for data in players_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON en {filename}: {e}")
        return []
