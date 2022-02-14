import gamelib


def interfaz_pokedex_completo(titulo):
    """ Muestra la interfaz de la pokedex generica y recibe por parametro el 
    titulo que se le quiera poner a la sección. """
    return gamelib.draw_rectangle(50, 50, 900, 650, fill='red'), \
        gamelib.draw_oval(80, 70, 130, 120, outline='black', fill='#15E8E8'), \
        gamelib.draw_oval(150, 70, 170, 90, outline='black', fill='red'), \
        gamelib.draw_oval(180, 70, 200, 90, outline='black', fill='green'), \
        gamelib.draw_oval(210, 70, 230, 90, outline='black', fill='yellow'), \
        gamelib.draw_rectangle(80, 150, 870, 550, fill='grey'), \
        gamelib.draw_rectangle(90, 160, 860, 540, fill='white'), \
        gamelib.draw_oval(80, 560, 120, 600, fill='blue'), \
        gamelib.draw_oval(150, 560, 180, 590, fill='green', outline='green'), \
        gamelib.draw_rectangle(165, 560, 235, 590, fill='green', outline='green'), \
        gamelib.draw_oval(220, 560, 250, 590, fill='green', outline='green'), \
        gamelib.draw_oval(290, 560, 320, 590, fill='yellow', outline='yellow'), \
        gamelib.draw_rectangle(305, 560, 375, 590, fill='yellow', outline='yellow'), \
        gamelib.draw_oval(360, 560, 390, 590, fill='yellow', outline='yellow'), \
        gamelib.draw_text(titulo, 400, 110, fill='white', anchor='nw', bold=True, size=20), \
        gamelib.draw_text(
            "Presiona la h para ver los comandos disponibles", 690, 620, fill="white", size=14)
