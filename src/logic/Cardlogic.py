from src.managers import CardDataManager
from src.ui.windowsconfig import CARTAS_CREADAS


# Función para verificar que un atributo es numérico
def atributonumero(atri):
    for i, entrada_atributo in enumerate(atri):
        try:
            a = int(entrada_atributo.get_text())
        except ValueError:
            return False
    return True

# Función para verificar que los valores de atributos estén en el rango permitido
def rangoatributos(atri):
    """Verifica si todos los valores en la lista de atributos están en el rango de -100 a 100. """
    for i, entrada_atributo in enumerate(atri):
        if not atributonumero(atri):
            return False

        a = entrada_atributo.get_text()
        # Convertir a int o float si es necesario, manejar errores si los hay
        try:
            a = int(a)  # o float(valor) si necesitas números decimales
        except ValueError:
            a = 0  # Manejo simple de errores
        if a not in range(-100, 101):
            return False
        return True


# Función para obtener los atributos ingresados y convertirlos en un diccionario
def getatr(atributo_entries, atributos):
    result = {}
    for i, entrada_atributo in enumerate(atributo_entries):
        valor = entrada_atributo.get_text()
        # Convertir a int o float si es necesario, manejar errores si los hay
        try:
            result[atributos[i]] = int(valor)  # o float(valor) si necesitas números decimales
        except ValueError:
            result[atributos[i]] = 0  # Manejo simple de errores
    return result


def Ncard():
    print("a")

#Verifica si los datos de la carta son válidos según las restricciones de longitud y rango.
def isvalid(manager, atributo_entries, nombre_personaje, descripcion, turno_poder, bonus_poder):
    mensaje = ""
    if not (len(nombre_personaje)) in range(5, 30):
        mensaje = "El nombre debe tener entre 5 y 30 caracteres intente de nuevo"
        return False, mensaje
    if len(descripcion) > 1000:
        mensaje = "La descripción no puede tener más de 1000 caracteres"
        return False, mensaje
    if not turno_poder in range(0, 100):
        mensaje = "El valor de turno de poder debe ser un número entre 0 y 100"
        return False, mensaje
    if not bonus_poder in range(0, 100):
        mensaje = "El valor de bonus de poder de poder debe ser un número entre 0 y 100"
        return False, mensaje
    if not rangoatributos(atributo_entries):
        mensaje = "Los atributos deben ser un número entre -100 y 100"
        return False, mensaje
    return True, ""



# Función para verificar si una carta ya existe en el sistema
def svariant(nombrecarta):
    #Verifica si una carta ya existe en el sistema al compararla con el nombre de cartas cargadas.
    cartas = CardDataManager.cargar_cartas_desde_json()
    for cartaexiste in cartas:
        if cartaexiste.get_nombrepersonaje() == nombrecarta:
            return "Si"
    return "No"

def savecard(nuevacarta):
    # Guardar cartas
    CARTAS_CREADAS.append(nuevacarta)
    print(f"Carta creada: {nuevacarta}")
    CardDataManager.guardar_cartas_en_json(CARTAS_CREADAS)

def generarcartas(album, cantidad_cartas):
    return CardDataManager.asignar_cartas_iniciales(album, cantidad_cartas=cantidad_cartas)

