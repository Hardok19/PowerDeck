from src.models.Carta import generar_llave_identificadora

class player():
    def __init__(self, name, alias, country, email, password, llave, esadmin, album, mazos):
        self.name = name
        self.alias = alias
        self.country = country
        self.email = email
        self.password = password
        self.esadmin = esadmin  # 0: Jugador, 1: Admin Control, 2: Admin Juego, 3: Superusuario
        if len(llave) < 4:
            self.llave = generar_llave_identificadora()
        else:
            self.llave = llave
        self.album = album
        self.mazos = mazos