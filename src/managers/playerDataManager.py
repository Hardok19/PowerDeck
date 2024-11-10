import json
from src.models.Album import playerAlbum



filename = '../data/players.json'

def player_to_dict(player):
    name, alias, country, email, password, album, mazos = player
    return {
        'name': name,
        'alias': alias,
        'country': country,
        'email': email,
        'password': password,
        'album': album.to_list(),
        'mazos': [{'nombre': nombre_mazo, 'album': mazo_album.to_list()} for nombre_mazo, mazo_album in mazos]
    }

def player_from_dict(data):
    name = data['name']
    alias = data['alias']
    country = data['country']
    email = data['email']
    password = data['password']
    album = playerAlbum.from_list(data['album'])
    mazos = [(mazo_data['nombre'], playerAlbum.from_list(mazo_data['album'])) for mazo_data in data['mazos']]
    return [name, alias, country, email, password, album, mazos]

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
