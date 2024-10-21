import CardDataManager




def svariant(nombrecarta):
    cartas = CardDataManager.cargar_cartas_desde_json()
    for cartaexiste in cartas:
        if cartaexiste == nombrecarta:
            return False
    return True

