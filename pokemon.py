import gamelib
import csv
import equipos
import pokedex

INSTRUCCIONES = 'h'

EQUIPOS = '2'

CANT_POKEMON = 151


def mostrar_pokedex(indice_pokemon_actual, lista_pokemon):
    """ Muestra las estadisticas de los pokemon """
    pokedex.interfaz_pokedex_completo("Pokemons")

    gamelib.draw_text(f"{lista_pokemon[indice_pokemon_actual]['nombre']}",
                      450, 160, fill='black', anchor='nw', bold=True, size=20)
    gamelib.draw_image(lista_pokemon[indice_pokemon_actual]['imagen'], 50, 165)
    gamelib.draw_text(f"HP: {lista_pokemon[indice_pokemon_actual]['hp']}",
                      600, 200, fill='black', anchor='nw', bold=True)
    gamelib.draw_text(
        f"Ataque: {lista_pokemon[indice_pokemon_actual]['atk']}", 600, 250, fill='black', anchor='nw', bold=True)
    gamelib.draw_text(
        f"Defensa: {lista_pokemon[indice_pokemon_actual]['def']}", 600, 300, fill='black', anchor='nw', bold=True)
    gamelib.draw_text(
        f"Ataque Especial: {lista_pokemon[indice_pokemon_actual]['spa']}", 600, 350, fill='black', anchor='nw', bold=True)
    gamelib.draw_text(
        f"Defensa Especial: {lista_pokemon[indice_pokemon_actual]['spd']}", 600, 400, fill='black', anchor='nw', bold=True)
    gamelib.draw_text(
        f"Velocidad: {lista_pokemon[indice_pokemon_actual]['spe']}", 600, 450, fill='black', anchor='nw', bold=True)


def busqueda_pokemon(indice_actual, diccionario_pokemon):
    """ Se busca por ID o por nombre un pokemon en especifico y se muestra """
    pokemon_a_buscar = gamelib.input(
        "¿Que pokemon queres buscar? (ID o nombre)")
    if not pokemon_a_buscar:
        return indice_actual
    pokemon_a_buscar = pokemon_a_buscar.capitalize()
    if pokemon_a_buscar.isnumeric():
        if int(pokemon_a_buscar) > len(diccionario_pokemon) or int(pokemon_a_buscar) == 0:
            gamelib.say("Ese ID no es valido, porfavor ingrese otro")
            return indice_actual
        return int(pokemon_a_buscar)-1
    if pokemon_a_buscar in diccionario_pokemon:
        return int(diccionario_pokemon.get(pokemon_a_buscar)["numero"]) - 1
    gamelib.say("Ese pokemon no existe, porfavor ingrese otro")
    return indice_actual


def leer_archivo_pokemon():
    diccionario_pokemon = {}
    lista_pokemon = []
    with open('pokemons.csv') as f:
        diccionario = csv.DictReader(f, delimiter=";")
        # Itero el resultado de DictReader() y guardo en forma de lista
        # de diccionarios y otra en forma de diccionario siendo la key el
        # nombre del Pokemon.
        for pokemon in diccionario:
            lista_pokemon.append(pokemon)
            diccionario_pokemon[pokemon["nombre"]] = pokemon
    return lista_pokemon, diccionario_pokemon


def main():
    indice_pokemon_actual = 0
    gamelib.resize(950, 700)

    lista_pokemon, diccionario_pokemon = leer_archivo_pokemon()
    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        mostrar_pokedex(indice_pokemon_actual, lista_pokemon)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()
        if not ev:
            # El usuario cerró la ventana.
            break

        """ APRETA Escape PARA CERRAR LA POKEDEX """
        if ev.type == gamelib.EventType.KeyPress:
            if ev.key == 'Escape':
                # El usuario presionó la tecla Escape, cerrar la aplicación.
                break
            """ APRETA FLECHA PARA LA IZQUIERDA PARA MOVERTE ENTRE LOS POKEMON """
            if ev.key == 'Left':
                # El usuario presionó la flecha izquierda.
                indice_pokemon_actual = (
                    indice_pokemon_actual - 1) % CANT_POKEMON

            """ APRETA FLECHA PARA LA DERECHA PARA MOVERTE ENTRE LOS POKEMON """
            if ev.key == 'Right':
                # El usuario presionó la flecha derecha.
                indice_pokemon_actual = (
                    indice_pokemon_actual + 1) % CANT_POKEMON

            """ APRETA h PARA VER LAS INSTRUCCIONES """
            if ev.key.lower() == INSTRUCCIONES:
                gamelib.say(
                    'INSTRUCCIONES\n\n Seccion Pokemons:\n\n -> : Siguiente pokemon \n <- : Pokemon anterior \n enter: Buscar pokemon \n 2: Ir a la seccion equipos')

            """ APRETA Return/Enter PARA BUSCAR POKEMON """
            if ev.key == 'Return':
                indice_pokemon_actual = busqueda_pokemon(
                    indice_pokemon_actual, diccionario_pokemon)

            """ APRETA 2 PARA CAMBIAR A LA SECCIÓN EQUIPOS """
            if ev.key == EQUIPOS:
                equipos.iniciar_equipos(lista_pokemon)


gamelib.init(main)
