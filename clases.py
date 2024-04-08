import numpy as np

class Jugador:
    """
    Representa un jugador en el juego de hundir la flota. 
    Maneja la creación de tableros, el posicionamiento de barcos y la verificación de adyacencia.
    """
    def __init__(self, id_jugador, sizes=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]):
        """
        Inicializa un jugador con un id, tamaños de barco por defecto, un tablero y un tablero de disparos.
        
        id_jugador: Identificador único para el jugador.
        sizes: Lista de enteros que representan los tamaños de los barcos.
        """
        self.id_jugador = id_jugador
        self.sizes = sizes
        self.tablero = np.full((10, 10), " ") # tablero con nuestros barcos
        self.tab_disparos = np.full((10, 10), " ") # tablero de seg de nuestros disparos
        self.coord_disp = [] # coordenadas de donde disparamos ( PTE )
        self.coord_barcos = [] # lista de diccionarios de cada barco

    def identificar_tipo_barco(self, size):
        """
        Identifica el tipo de barco según en su tamaño.
        
        size: El tamaño del barco.
        -> return: Nos devuelve el nombre del barco.
        """
        tipos_barco = {1: "Fragata", 2: "Destructor", 3: "Submarino", 4: "Acorazado"}
        return tipos_barco[size]

    def reset_tablero(self):
        """
        Reinicia el tablero del jugador y la lista de coordenadas de los barcos.
        """
        self.tablero = np.full((10, 10), " ")
        self.coord_barcos = []

    def adyacencia(self, inicio, fin, orientacion):
        """
        Verifica la adyacencia de un barco para asegurarse de que no se coloque junto a otro incluyendo diagonalmente.
        
        inicio: Coordenadas de inicio del barco.
        fin: Coordenadas de fin del barco.
        orientacion: Orientación del barco ("horizontal" o "vertical").
        --> return: True si el barco puede colocarse, False en caso contrario.
        """

        # Calculamos los rangos de coordenadas a verifcar segun la horientacion del barco
        if orientacion == "horizontal":
            rango_x = (max(0, inicio[0] - 1), min(self.tablero.shape[0], inicio[0] + 2))
            rango_y = (max(0, inicio[1] - 1), min(self.tablero.shape[1], fin[1] + 2))
        else:
            rango_x = (max(0, inicio[0] - 1), min(self.tablero.shape[0], fin[0] + 2))
            rango_y = (max(0, inicio[1] - 1), min(self.tablero.shape[1], inicio[1] + 2))

        for x in range(rango_x[0], rango_x[1]):
            for y in range(rango_y[0], rango_y[1]):
                if self.tablero[x, y] == "B":
                    return False
        return True

    def reg_coord_barcos(self, size, inicio, orientacion):
        """
        Registra las coordenadas de los barcos colocados en el tablero.
        
        size: Tamaño del barco.
        inicio: Coordenadas de inicio del barco.
        orientacion: Orientación del barco.
        """
        # Obtenemos el nombre del barco
        tipo_barco = self.identificar_tipo_barco(size) 
        # cada uno tendrá un diccionario individual,  con sus coordenadas como lista de tuplas y un False por cada coordenada que tenga
        barco = {'tipo': tipo_barco, 'coordenadas': [], 'golpes': []}  
        coord1, coord2 = inicio # PTE usamos o no..
        # segun la orienzacion modificamos fila o cooordenadas
        if orientacion == "horizontal":
            for i in range(size):
                coordenada = (coord1, coord2 + i)
                barco['coordenadas'].append(coordenada)
                barco['golpes'].append(False)
        else:
            for i in range(size):
                coordenada = (coord1 + i, coord2)
                barco['coordenadas'].append(coordenada)
                barco['golpes'].append(False)
        self.coord_barcos.append(barco) #añadimos el diccionario barco a coord_barcos

    def colocar_barcos(self):
        """
        Coloca todos los barcos en el tablero de forma aleatoria y verifica la adyacencia.
        """
        self.reset_tablero() #reseteamos el tablero
        for size in self.sizes:
            situado = False
            while not situado:
                orientacion = "horizontal" if np.random.randint(0, 2) == 0 else "vertical"
                if orientacion == "horizontal":
                    coord1 = np.random.randint(0, 10)
                    coord2 = np.random.randint(0, 10 - size + 1)
                else:
                    coord1 = np.random.randint(0, 10 - size + 1)
                    coord2 = np.random.randint(0, 10)

                inicio = (coord1, coord2)
                fin = (coord1, coord2 + size - 1) if orientacion == "horizontal" else (coord1 + size - 1, coord2)

                if self.adyacencia(inicio, fin, orientacion):
                    if orientacion == "horizontal":
                        self.tablero[coord1, coord2:coord2 + size] = "B"
                    else:
                        self.tablero[coord1:coord1 + size, coord2] = "B"
                    self.reg_coord_barcos(size, inicio, orientacion)
                    situado = True

    def ganador(self):
        """
        Verifica si todos los barcos han sido completamente golpeados.
        
        --> return: True si todos los barcos han sido hundidos, False en caso contrario.
        """
        for barco in self.coord_barcos:
            if not all(barco['golpes']): #comprobamos la lista de boleanos de cada barco
                return False
        return True

class Humano(Jugador):
    """
    Representa a un jugador carnico, cuyo ataque se realiza a traves de inputs
    """
    def __init__(self, id_jugador, sizes=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]):
        super().__init__(id_jugador, sizes)

    def ataque_humano(self, enemigo):
        """
        Realiza un ataque en el tablero del enemigo basado en coordenadas elegidas por el usuario.
        
        enemigo: Instancia del jugador enemigo.
        --> return: True si el ataque resultó en un acierto, False en caso contrario.
        """

        acierto = False  # Con esta variable controlamos si hay acierto o no

        while True:  # mientras sigamos acertando, repetiremos
            print(self.tab_disparos)
            fila = int(input("Fila a disparar? (Entre 0 y 9): "))
            columna = int(input("Columna a disparar? (Entre 0 y 9): "))
            coord_disparo = (fila, columna)

            if coord_disparo in self.coord_disp: # Comprobacion de coordenadas repetidas
                print("Capitán, aquí ya hemos bombardeado previamente. Deme otras coordenadas:")
                continue  # Vuelve al inicio del bucle si las coordenadas ya se han utilizado

            self.coord_disp.append(coord_disparo)

            for barco in enemigo.coord_barcos:
                if coord_disparo in barco['coordenadas']:
                    index = barco['coordenadas'].index(coord_disparo)
                    barco['golpes'][index] = True
                    print(f"{coord_disparo} -> Tocado!")
                    self.tab_disparos[fila, columna] = "X"
                    enemigo.tablero[fila, columna] = "X"
                    acierto = True
                    if all(barco['golpes']):
                        print(f"¡Hundido! Has destrozado el {barco['tipo']} de Skinet.")
                    break  # Salimos del bucle for ya que encontramos el barco golpeado
            else:
                # Si el disparo no coincide con ninguna coordenada de los barcos, es agua
                print(f"{coord_disparo} -> Agua")
                self.tab_disparos[fila, columna] = "a"
                enemigo.tablero[fila, columna] = "a"
            break  # Salimos del bucle while luego de un disparo, acertado o no

        return acierto  # Retornamos si ha sido un acierto para determinar si se sigue jugando o cambia el turno

class Maquina(Jugador):
    """
    Representa a un jugador no carnico, cuyo ataque se realiza de forma aleatoria en todo momento
    """
    def __init__(self, id_jugador):
        super().__init__(id_jugador)

    def ataque_maquina(self, enemigo):
        """
        Realiza un ataque  en el tablero del enemigo eligiendo coordenadas al azar.
        
        enemigo: jugador enemigo que definimos en la clase Juego
        --> return: True si el ataque resultó en un acierto, False en caso contrario.
        """
        acierto = False  # Esta variable controlará si la máquina ha acertado su disparo
        while True:
            fila = np.random.randint(0, 10)
            columna = np.random.randint(0, 10)
            coord_disparo = (fila, columna)

            if coord_disparo not in self.coord_disp:
                self.coord_disp.append(coord_disparo)
                print(f"Skinet ha disparado en el {fila}, {columna}")
                for barco in enemigo.coord_barcos:
                    if coord_disparo in barco['coordenadas']:
                        index = barco['coordenadas'].index(coord_disparo)
                        barco['golpes'][index] = True
                        print(f"{coord_disparo} -> Tocado! Skinet ha acertado.")
                        self.tab_disparos[fila, columna] = "X"
                        enemigo.tablero[fila, columna] = "X"
                        acierto = True
                        if all(barco['golpes']):
                            print(f"¡Hundido! Skinet ha destrozado el {barco['tipo']}.")
                        break  # Salimos del bucle for ya que encontramos el barco golpeado
                else:
                    # Si el disparo no coincide con ninguna coordenada de los barcos, es agua
                    print(f"{coord_disparo} -> Agua")
                    self.tab_disparos[fila, columna] = "a"
                    enemigo.tablero[fila, columna] = "a"

                print(enemigo.tablero)
                break  # Salimos del bucle while luego de un disparo, acertado o no
        return acierto  # Retornamos si ha sido un acierto para determinar si se sigue jugando o cambia el turno

class Maquina_de_matar(Maquina):
    """
    Representa a un jugador no carnico de IA avanzada, cuyo ataque se realiza de forma aleatoria hasta que acierta en un objetivo, 
    en cuyo caso lo perseguira hasta su exterminio.
    """
    def __init__(self, id_jugador):
        super().__init__(id_jugador)
        self.ultimo_acierto = None  # Almacena la última posición acertada para enfocar los siguientes disparos alrededor.

    def sig_objetivo(self):
        """
        Elige el siguiente objetivo basado en el último acierto, si lo hay, para maximizar la efectividad del ataque.
        
        --> return: Las coordenadas del siguiente disparo.
        """
        if self.ultimo_acierto:
            fila, columna = self.ultimo_acierto
            # Genera posibles objetivos alrededor del último acierto
            posibles_objetivos = [
                (max(fila - 1, 0), columna), (min(fila + 1, 9), columna),
                (fila, max(columna - 1, 0)), (fila, min(columna + 1, 9))
            ]
            np.random.shuffle(posibles_objetivos)  # Mezcla los objetivos para añadir algo de aleatoriedad
            for objetivo in posibles_objetivos:
                if objetivo not in self.coord_disp:
                    return objetivo
        # Si no hay último acierto o no se encontraron objetivos válidos, elige aleatoriamente
        return np.random.randint(0, 10), np.random.randint(0, 10)

    def ataque_maquina(self, enemigo):
        """
        Realiza un ataque utilizando la estrategia de 'Maquina_de_matar' para elegir el objetivo.
        
        enemigo: jugador enemigo que definimos en la clase Juego
        --> True si el ataque resultó en un acierto, False en caso contrario.
        """
        # igual que ataque_maquina, pero implementamos "elegir sig objetivo"
        acierto = False
        while True:
            fila, columna = self.sig_objetivo()
            coord_disparo = (fila, columna)

            if coord_disparo not in self.coord_disp:
                self.coord_disp.append(coord_disparo)
                print(f"Maquina_de_matar ha disparado en el {fila}, {columna}")
                for barco in enemigo.coord_barcos:
                    if coord_disparo in barco['coordenadas']:
                        index = barco['coordenadas'].index(coord_disparo)
                        barco['golpes'][index] = True
                        print(f"{coord_disparo} -> Tocado! Maquina_de_matar ha acertado.")
                        self.tab_disparos[fila, columna] = "X"
                        enemigo.tablero[fila, columna] = "X"
                        self.ultimo_acierto = coord_disparo  # Actualiza el último acierto
                        acierto = True
                        if all(barco['golpes']):
                            print(f"¡Hundido! Maquina_de_matar ha destrozado el {barco['tipo']}.")
                            self.ultimo_acierto = None  # Restablece el último acierto si el barco está hundido
                        break
                else:
                    print(f"{coord_disparo} -> Agua")
                    self.tab_disparos[fila, columna] = "a"
                    enemigo.tablero[fila, columna] = "a"
                    if not acierto:  # Si no ha habido un acierto, limpia el último acierto
                        self.ultimo_acierto = None
                print(enemigo.tablero)
                break
        return acierto


class Juego:
    """
    Gestiona el flujo del juego, manejando los jugadores y la lógica de juego principal.
    """
    def __init__(self):
        """
        Inicializa el juego creando un jugador humano y dejando espacio para un jugador máquina que será definido por la dificultad.
        """
        self.humano = Humano("Jugador 1")
        self.maquina = None

    def elegir_dificultad(self):
        """
        Permite al jugador elegir la dificultad del juego, que determina el tipo de jugador máquina (Maquina o Maquina_de_matar).
        """
        dificultad = int(input("Elige el nivel de : Fácil (1) o Difícil (2): "))
        if dificultad == 1:
            self.maquina = Maquina_de_matar("Skinet")
        elif dificultad == 2:
            self.maquina = Maquina("Skinet")
        else:
            # Si se introduce un valor inválido, por defecto se elige la dificultad fácil
            print("Dificultad no reconocida. Seleccionando dificultad Fácil por defecto.")
            self.maquina = Maquina("Skinet")
            #PTE: introducir control para letras.

    def iniciar_juego(self):
        """
        Inicia el juego, incluyendo la elección de dificultad, colocación de barcos, y determinación de quién inicia el juego.
        """
        print("Bienvenido a Hundir la Flota!")
        self.elegir_dificultad() # Elegimos el nivel de dificulta que tendrá la Maquina
        self.humano.colocar_barcos()
        print("Este es tu tablero")
        print(self.humano.tablero)
        self.maquina.colocar_barcos() #PTE: quitar cuando y esté todo ok.
        print("Tablero de Skinet")
        print(self.maquina.tablero)

        respuesta = int(input("¿Quién quieres que empiece primero: (1)Tú, (2)Máquina, (0)Aleatorio? "))
        if respuesta == 1:
            self.jugar(True)
        elif respuesta == 2:
            self.jugar(False)
        else:
            self.jugar(np.random.choice([True, False]))
            #PTE: introducir control para letras.

    def jugar(self, turno_humano):
        """
        Ejecuta el bucle principal del juego, alternando turnos entre el jugador humano y la máquina hasta que haya un ganador.
        
        --> turno_humano: Un booleano que determina si el jugador humano comienza el juego.
        """
        while True:
            if turno_humano:
                acierto = self.humano.ataque_humano(self.maquina)
            else:
                acierto = self.maquina.ataque_maquina(self.humano)

            if acierto: # Verificamos si el juego ha terminado después de cada acierto
                if self.humano.ganador() or self.maquina.ganador():
                    ganador = "Humano" if self.humano.ganador() else "Máquina"
                    print(f"El juego ha terminado. ¡El ganador es {ganador}!")
                    break
                else:
                    print("Dispara de nuevo.")
                    print("Pulsa Intro para continuar.")
                    input()
                    continue
            else: # Cambiamos de turno cuando algun jugador no acierte
                turno_humano = not turno_humano
                print("Pulsa Intro para continuar.")
                input()
