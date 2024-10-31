import CardDataManager


def rangoatributos(atri):
    for i, entrada_atributo in enumerate(atri):
        if not entrada_atributo.get_text().isnumeric():
            return False

        a = entrada_atributo.get_text()
        # Convertir a int o float si es necesario, manejar errores si los hay
        try:
            a = int(a)  # o float(valor) si necesitas números decimales
        except ValueError:
            a = 0  # Manejo simple de errores
        if a not in range(-100, 100):

            return False
    return True

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




def svariant(nombrecarta):
    cartas = CardDataManager.cargar_cartas_desde_json()
    for cartaexiste in cartas:
        if cartaexiste == nombrecarta:
            return False
    return True


