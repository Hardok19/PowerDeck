import json
from Admin import Admin  # Asegúrate de tener la clase Admin definida en Admin.py

def load_admins(filename='admins.json'):
    try:
        with open(filename, 'r') as f:
            admins_data = json.load(f)
        return [Admin.from_dict(admin_data) for admin_data in admins_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_admins(admins, filename='admins.json'):
    admins_data = [admin.to_dict() for admin in admins]
    with open(filename, 'w') as f:
        json.dump(admins_data, f, indent=4)