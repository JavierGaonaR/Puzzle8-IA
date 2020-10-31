import random
import copy


def crea_puzzle():
    puzzle = [[0, 2, 3], [1, 4, 6], [7, 5, 8]]
    random.shuffle(puzzle[0])
    random.shuffle(puzzle[1])
    random.shuffle(puzzle[2])
    random.shuffle(puzzle[random.randint(0, 2)])
    return puzzle


def movimientos(puzzle, predecesor):
    hijos = []

    if 0 in puzzle[0]:
        i = 0
        j = puzzle[0].index(0)

    elif 0 in puzzle[1]:
        i = 1
        j = puzzle[1].index(0)

    else:
        i = 2
        j = puzzle[2].index(0)

    hijo1 = copy.deepcopy(puzzle)
    hijo2 = copy.deepcopy(puzzle)
    hijo3 = copy.deepcopy(puzzle)
    hijo4 = copy.deepcopy(puzzle)

    if j + 1 < len(hijo1[0]):
        y = hijo1[i][j]
        hijo1[i][j] = hijo1[i][j+1]
        hijo1[i][j+1] = y

    if j - 1 >= 0:
        y = hijo2[i][j]
        hijo2[i][j] = hijo2[i][j-1]
        hijo2[i][j-1] = y

    if i + 1 < len(hijo3):
        y = hijo3[i][j]
        hijo3[i][j] = hijo3[i+1][j]
        hijo3[i+1][j] = y

    if i - 1 >= 0:
        y = hijo4[i][j]
        hijo4[i][j] = hijo4[i-1][j]
        hijo4[i-1][j] = y

    if hijo1 != puzzle:
        hijos.append(hijo1)

    if hijo2 != puzzle:
        hijos.append(hijo2)

    if hijo3 != puzzle:
        hijos.append(hijo3)

    if hijo4 != puzzle:
        hijos.append(hijo4)

    return hijos


def Bfs(puzzle, solucion):
    nivel = 0
    arbol = {nivel: puzzle}
    hijos = movimientos(puzzle, "null")
    nivel += 1
    arbol[nivel] = hijos
    while nivel < 500:
        nivel = nivel + 1
        for i in hijos:
            hijos2 = movimientos(i, "null")
            if solucion in hijos:
                return hijos, True
            if nivel not in arbol:
                arbol[nivel] = hijos2
            else:
                arbol[nivel].append(hijos2)
        hijos[:] = []
        for j in hijos2:
            hijos.append(j)
        hijos2[:] = []
    return arbol, False


def Dfs(puzzle, solucion):
    nivel = 0
    arbol = {nivel: puzzle}
    hijos = movimientos(puzzle, "null")
    nivel += 1

    arbol[nivel] = hijos
    explorado = list()

    stack = [copy.deepcopy(puzzle)]

    while nivel < 1000:
        nodo_actual = stack.pop()
        nivel = nivel + 1

        for tmp in movimientos(puzzle, "null"):
            stack.append(tmp)

        explorado.append([nodo_actual])

        if solucion in nodo_actual:
            return arbol, True

        hijos = copy.deepcopy(movimientos(nodo_actual, "null"))

        for hijo in hijos:
            if hijo not in explorado:
                stack.append(hijo)
                explorado.append([hijo])
                if nivel not in arbol:
                    arbol[nivel] = hijo
                else:
                    arbol[nivel].append(hijo)

        nodo_actual = []
    return arbol, False


def aStar(puzzle, solucion):
    nivel = 0
    arbol = {nivel: puzzle}
    hijos = movimientos(puzzle, "null")
    nivel += 1

    explorado = list()

    stack = copy.deepcopy([puzzle])

    hInicial = h(puzzle, solucion)

    while nivel < 10000:
        nodo_actual = stack.pop()
        nivel = nivel + 1

        for tmp in movimientos(puzzle, "null"):
            stack.append(tmp)

        explorado.append([nodo_actual])

        if solucion in nodo_actual:
            return arbol, True

        hijos = copy.deepcopy(movimientos(nodo_actual, "null"))

        for hijo in hijos:
            hActual = h(hijo, solucion)
            if hActual == 0:
                if nivel not in arbol:
                    arbol[nivel] = hijo
                else:
                    arbol[nivel].append(hijo)
                return arbol, True
            elif hActual < hInicial:
                hInicial = hActual
                stack.append(hijo)
                explorado.append([hijo])
                if nivel not in arbol:
                    arbol[nivel] = hijo
                else:
                    arbol[nivel].append(hijo)
                break

        nodo_actual = []
    return arbol, False


def hillClimbing(puzzle, solucion):
    stack = copy.deepcopy([puzzle])
    nivel = 0
    arbol = {nivel: puzzle}

    while nivel < 1000:

        if len(stack) <= 0:
            return arbol, False

        state = stack.pop()

        nivel += 1

        if state == solucion:
            return arbol, True

        h_val = h(state, solucion)
        next_state = False

        hijos = movimientos(state, "null")

        for hijo in hijos:
            h_val_sig = h(hijo, solucion)

            # El algoritmo continua solo si se tiene una h(x) igual o menor con una h(x)_siguiente menor o igual
            # de otra menera el algoritmo se detiene.
            if h_val_sig <= h_val and not hijo in arbol.values():
                next_state = copy.deepcopy(hijo)
                h_val = h_val_sig
                stack.append(next_state)

                if nivel not in arbol:
                    arbol[nivel] = hijo
                else:
                    arbol[nivel].append(hijo)
                break

    return arbol, False


def h(puzzle, solucion):
    temp = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i][j] != solucion[i][j] and solucion[i][j] != '0':
                temp += 1

    return temp


cant = 0
solucion = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

while True:
    op = int(input(
        "Seleccione el modelo\n\n\t1) Dfs\n\t2) A* Search\n\t3) Bfs\n\t4) Hill Climbing\n\t0) Salir\n\n\nOpcion: "))

    if op == 1 or op == 3:
        print("Solucion: ", solucion)
        for j in range(0, 10):
            for i in range(0, 10):
                puzzle = crea_puzzle()
                if op == 1:
                    res, flag = Dfs(puzzle, solucion)
                elif op == 3:
                    res, flag = Bfs(puzzle, solucion)
                if flag:
                    cant = cant + 1
                print("Puzzle: ", res)
            print("Vuelta: ", j+1, " Cantidad: ", cant)
            print("-"*60)
        promedio = cant / 10
        print("Promedio: ", promedio)
    elif op == 2 or op == 4:
        print("Solucion: ", solucion)
        for j in range(0, 10):
            puzzle = crea_puzzle()
            if op == 2:
                res, flag = aStar(puzzle, solucion)
            if op == 4:
                res, flag = hillClimbing(puzzle, solucion)
            if flag:
                cant = cant + 1
            print("Puzzle: ")
            for i in res:
                print(res[i])
        print("Vuelta: ", j+1, " Cantidad: ", cant)
        print("-"*60)
        promedio = cant / 10
        print("Promedio: ", promedio)
    elif op == "0":
        break
    else:
        print("Caracter incorrecto")
