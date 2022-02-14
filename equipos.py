import gamelib
import csv
import pokedex

AGREGAR_POKEMON = 'p'
ELIMINAR_POKEMON = 'x'
INSTRUCCIONES = 'h'
AGREGAR_EQUIPO = 'e'

ARCHIVO_MOVIMIENTOS = 'movimientos.csv'

POKEDEX = '1'

MAXIMO_MOVIMIENTOS = 4
MAXIMO_POKEMONS = 6


def mensaje_agregar_equipo(i, posicion_x, posicion_y):
    """ Muestra en pantalla el mensaje de 'Agregar pokemon' """
    for _ in range(i):
        gamelib.draw_text(f"Agregar Pokemon para completar el equipo",
                          posicion_x, posicion_y, fill='black', anchor='nw', bold=True)
        posicion_y += 50


def mostrar_pokedex(indice_equipo_actual, equipos, nombre, posicion_x=100, posicion_y=250):
    """ Muestra en pantalla los equipos """
    pokedex.interfaz_pokedex_completo("Equipos")
    if not nombre:
        gamelib.draw_text(f"Presiona la e para agregar un equipo!",
                          220, 160, fill='black', anchor='nw', bold=True, size=20)
    else:
        gamelib.draw_text(f"Equipo {nombre[indice_equipo_actual]}",
                          370, 160, fill='black', anchor='nw', bold=True, size=20)

        if len(equipos[indice_equipo_actual]) == 0:
            mensaje_agregar_equipo(MAXIMO_POKEMONS, posicion_x, posicion_y)
        else:
            posicion_y_actual = posicion_y
            for i in range(len(equipos[indice_equipo_actual])):
                for pokemon, movimientos in equipos[indice_equipo_actual][i].items():
                    mensaje = pokemon + ': ' + ', '.join(movimientos)
                    gamelib.draw_text(
                        f"{mensaje}", posicion_x, posicion_y, fill='black', anchor='nw', bold=True)
                    posicion_y += 50
                    posicion_y_actual += 50
            mensaje_agregar_equipo(
                MAXIMO_POKEMONS - len(equipos[indice_equipo_actual]), posicion_x, posicion_y_actual)


def existe_el_pokemon(pokemons, pokemon_nuevo):
    """ Verifica si el pokemon esta agregado al equipo """
    if pokemon_nuevo in pokemons:
        gamelib.say(
            "el pokemon seleccionado ya existe en tu equipo, elige otro pokemon")
        return True
    return False


def pokemon_valido(pokemon_a_agregar, pokemons_validos):
    """ Se fija si el pokemon es valido o no para ser agregado """
    for i in range(len(pokemons_validos)):
        if pokemon_a_agregar == pokemons_validos[i]['nombre']:
            return True

    gamelib.say("Pokemon invalido")
    return False


def mostrar_movimientos(lista_movimientos):
    """ Muestra en pantalla los movimientos posibles para cada pokemon """
    texto_imprimir = ""
    for i in range(len(lista_movimientos)):
        if not i % 6 == 0:
            texto_imprimir += f" {lista_movimientos[i]} -"
        else:
            texto_imprimir += "\n"

    return texto_imprimir


def agregar_pokemon_equipo(equipos, pokemons, lista_pokemon_validos, dict_pokemon_movimientos):
    """ Agrega un pokemon con sus ataques """
    movimientos_elegidos = []

    pokemon_a_agregar = gamelib.input("Agregar Pokemon")
    if not pokemon_a_agregar:
        return equipos, pokemons
    pokemon_a_agregar = pokemon_a_agregar.capitalize()
    if not existe_el_pokemon(pokemons, pokemon_a_agregar) and pokemon_valido(pokemon_a_agregar, lista_pokemon_validos):
        pokemons.append(pokemon_a_agregar)
        movimientos_posibles = dict_pokemon_movimientos.get(
            pokemon_a_agregar, [])

        while len(movimientos_elegidos) == 0 or len(movimientos_elegidos) < MAXIMO_MOVIMIENTOS:
            movimiento_a_agregar = gamelib.input(
                f"¿Que movimiento queres agregar?\n{mostrar_movimientos(movimientos_posibles)}")
            if movimiento_a_agregar == None:
                if len(movimientos_elegidos) == 0:
                    gamelib.say("El pokemon debe tener al menos un movimiento")
                    continue
                else:
                    break
            elif movimiento_a_agregar == '' or movimiento_a_agregar == ' ':
                gamelib.say(
                    "Movimiento inexistente, porfavor elija un movimiento valido")
                continue
            elif movimiento_a_agregar not in movimientos_posibles:
                gamelib.say("Este Pokemon no tiene ese ataque.")
            elif movimiento_a_agregar in movimientos_elegidos:
                gamelib.say("El pokemon ya tiene ese ataque.")
            else:
                movimientos_elegidos.append(movimiento_a_agregar)

        equipos.append({pokemon_a_agregar: movimientos_elegidos})
        return equipos, pokemons

    return equipos, pokemons


def leer_archivo_equipos():
    """ leer_archivo_equipos abre el archivo equipos.csv donde estan guardados los equipos creados por el usuario
    usando csv.DictReader y recupera los datos del ultimo guardado """
    nombres_equipos = []
    equipos = []
    pokemons_equipo_actual = []
    with open('equipos.csv') as f:
        diccionario = csv.DictReader(f, delimiter=";")
        lista_equipos_archivados = list(diccionario)
        equipo_actual = 0
        equipos.append([])
        pokemons_equipo_actual.append([])
        if len(lista_equipos_archivados) != 0 and lista_equipos_archivados[0]['id_equipo'] == '0':
            nombres_equipos.append(
                lista_equipos_archivados[0]['nombre_equipo'])

        for pokemon in lista_equipos_archivados:
            if pokemon['id_equipo'] == str(equipo_actual):
                equipos[equipo_actual].append(
                    {pokemon['pokemon']: pokemon['movimientos'].split(',')})
                pokemons_equipo_actual[equipo_actual].append(
                    pokemon['pokemon'])
            else:
                equipo_actual += 1
                equipos.append([])
                pokemons_equipo_actual.append([])
                nombres_equipos.append(pokemon['nombre_equipo'])
                equipos[equipo_actual].append(
                    {pokemon['pokemon']: pokemon['movimientos'].split(',')})
                pokemons_equipo_actual[equipo_actual].append(
                    pokemon['pokemon'])
                continue
        if len(equipos) > 1 and len(equipos[0]) == 0:
            equipos.pop(0)
        return equipos, pokemons_equipo_actual, nombres_equipos

def leer_archivo_movimientos(archivo):
    ''' Esta función lee el archivo y devuelve un diccionario que es clave: Pokemon, 
    valor: movimientos posibles de ese Pokemon '''
    diccionario_pokemon_movimientos = {}
    with open(archivo) as f:
        lector = csv.reader(f, delimiter=";")
        next(lector)
        for pokemon, movimientos in lector:
            diccionario_pokemon_movimientos[pokemon] = diccionario_pokemon_movimientos.get(
                pokemon, movimientos.split(","))
    return diccionario_pokemon_movimientos


def eliminar_pokemon(pokemons_equipo_actual, indice_equipo_actual, equipos):
    pokemon_a_eliminar = gamelib.input(
        "¿Qué pokemon queres eliminar de tu equipo?")
    if not pokemon_a_eliminar:
        return
    pokemon_a_eliminar = pokemon_a_eliminar.capitalize()
    if pokemon_a_eliminar not in pokemons_equipo_actual[indice_equipo_actual]:
        gamelib.say('Ese pokemon no existe en tu equipo')
        return

    for i in range(len(equipos[indice_equipo_actual])):
        if pokemon_a_eliminar in equipos[indice_equipo_actual][i]:
            equipos[indice_equipo_actual].pop(i)
            pokemons_equipo_actual[indice_equipo_actual].pop(i)
            break


def guardar_cambios(equipos, nombres_equipos):
    with open('equipos.csv', 'w', newline="") as csvfile:
        fieldnames = ['id_equipo', 'nombre_equipo', 'pokemon', 'movimientos']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        equipo_actual = 0

        writer.writeheader()
        while equipo_actual < len(equipos):
            for i in range(len(equipos[equipo_actual])):
                for pokemon, movimientos in equipos[equipo_actual][i].items():
                    writer.writerow({'id_equipo': equipo_actual, 'nombre_equipo': nombres_equipos[
                                    equipo_actual], 'pokemon': pokemon, 'movimientos': ','.join(movimientos)})
            equipo_actual += 1


def agregar_equipo(equipos, pokemons_equipo_actual, nombres_equipos, indice_equipo_actual):
    equipo_a_agregar = gamelib.input(
        "Elija el nombre de su nuevo equipo")
    if equipo_a_agregar:
        equipos.append([])
        pokemons_equipo_actual.append([])
        nombres_equipos.append(equipo_a_agregar)
        indice_equipo_actual += 1
    else:
        gamelib.say(
            'Por favor elija un nombre valido para su equipo')


def iniciar_equipos(lista_pokemon_validos):
    gamelib.resize(950, 700)

    indice_equipo_actual = 0
    dict_pokemon_movimiento = leer_archivo_movimientos(ARCHIVO_MOVIMIENTOS)

    try:
        equipos, pokemons_equipo_actual, nombres_equipos = leer_archivo_equipos()
    except IOError:
        with open('equipos.csv', 'w') as csvfile:
            fieldnames = ['id_equipo', 'nombre_equipo',
                          'pokemon', 'movimientos']
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()
            equipos, pokemons_equipo_actual, nombres_equipos = leer_archivo_equipos()

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        mostrar_pokedex(indice_equipo_actual, equipos, nombres_equipos)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        """ APRETA 1 PARA VOLVER A LA POKEDEX """
        if ev.type == gamelib.EventType.KeyPress:
            if ev.key == POKEDEX or ev.key == 'Escape':
                # El usuario presionó la tecla Escape, cerrar la aplicación.
                break

            """ APRETA LA p PARA AGREGAR POKEMON AL EQUIPO """
            if ev.key.lower() == AGREGAR_POKEMON:
                equipos[indice_equipo_actual], pokemons_equipo_actual[indice_equipo_actual] = agregar_pokemon_equipo(
                    equipos[indice_equipo_actual], pokemons_equipo_actual[indice_equipo_actual], lista_pokemon_validos, dict_pokemon_movimiento)
                guardar_cambios(equipos, nombres_equipos)

            """ APRETA h PARA VER LAS INSTRUCCIONES """
            if ev.key.lower() == INSTRUCCIONES:
                gamelib.say(
                    'INSTRUCCIONES\n\n Seccion equipo:\n\n p : Agregar pokemon equipo \n x : Elimminar pokemon de equipo \n e : Crear equipo \n 1: Ir a la pokedex')

            """ APRETA x PARA ELIMINAR POKEMON """
            if ev.key.lower() == ELIMINAR_POKEMON:
                eliminar_pokemon(pokemons_equipo_actual,
                                 indice_equipo_actual, equipos)
                guardar_cambios(equipos, nombres_equipos)

            """ APRETA e PARA AGREGAR EQUIPO """
            if ev.key.lower() == AGREGAR_EQUIPO:
                agregar_equipo(equipos, pokemons_equipo_actual,
                               nombres_equipos, indice_equipo_actual)

            if len(equipos) != 1:
                if ev.key == 'Left':
                    # El usuario presionó la flecha izquierda.
                    indice_equipo_actual = (
                        indice_equipo_actual - 1) % len(nombres_equipos)

                # if ev.type == gamelib.EventType.KeyPress and ev.key == 'e':
                    # prueba_seccion_equipos.interfaz_pokedex_completo()

                if ev.key == 'Right':
                    # El usuario presionó la flecha derecha.
                    indice_equipo_actual = (
                        indice_equipo_actual + 1) % len(nombres_equipos)

    '''Guardamos cambios cuando se cierra el programa, 
    cuando se elimina o agregar un pokemon'''
    guardar_cambios(equipos, nombres_equipos)
