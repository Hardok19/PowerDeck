class Admin:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # Considera encriptar las contraseñas para mayor seguridad
        self.role = role  # 'game_admin' o 'control_admin'

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data['username'],
            password=data['password'],
            role=data['role']
        )