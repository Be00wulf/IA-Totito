import sys
import pygame
import numpy as np


pygame.init()


#Colores
WHITE = (255, 255, 255)
GRAY = (45, 106, 79)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK = (8,28,21)


#PROPORCIONES Y TAMANIOS
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25


#PANTALLA INICIAL
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TOTITO AI')
screen.fill(DARK)


#este campo esta vacio y no esta usado -> tablero logico 
board = np.zeros((BOARD_ROWS, BOARD_COLS))


#para colorear el tablero cuando gane, pierda o empate. Dibuja una linea con un color desde-hasta
def draw_lines(color=WHITE):
    for i in range (1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


#dibujando una figura en una posicion del tablero
def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, 
                                #    center:
                                (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                           int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,                                 
                                #  start_pos:
                                (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4 ),
                                #  end_pos
                                (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                CROSS_WIDTH)
                
                pygame.draw.line(screen, color, 
                                #  start_pos:
                                (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4 ),
                                #  end_pos:
                                (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                CROSS_WIDTH)
                

#tomando row y col del tablero, para establecer player en un espacio 
def mark_square(row, col, player):
    board[row][col] = player


#revisar si el espacio esta vacio
def available_square(row, col):
    return board[row][col] == 0


#puede recibir cualquier tablero como argumento, el actual o el simulado por minimax
def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True


#verificar si se ha ganado: 3 en columna, 3 en fila o 3 en diagonal de un mismo player
def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False


#inicio de MINIMAX:
# El algoritmo de MINIMAX puede maximizar o no, y la razon por la que no siempre se deben maximizar las
    # puntuaciones es porque la computadora también debe adivinar el siguiente tiro que hara una persona
# Lo que hace una compu cuando hago un movimiento, esta piensa en lo que sucederia si hace uno u otro movimiento.
    # Esto lo hace por ejemplo, cuando comienzo tirando un circulo, la computadora considera todas las posibilidades
    # algo como que sucederia si responde con un tiro en una u otra celda
# Para determinar qué tan buena es una posibiliad, realiza la accion y luego simula lo que sucederia despues 
    # simula como si estuviera jugando consigo misma la IA para responder de uno u otro modo
# Es como un ciclo infinito de -puedo hacer esto y el puede hacer aquello- entonces se repite -puedo hacer esto y el 
    # puede hacer aquello-
    # Se pasan por toddas las posibilidades y le asigna puntuaciones, luego elige la mejor ruta para ganar 


#llamamos la funcion recursivamente desde las diferentes perspectivas hasta que llega a una victoria/derrota o empate
    #para volver a la llamada inicial para devolver la puntuación de toda la interacción
# Lo importante es evaluar que tan bueno es un movimiento
# funcion de evaluacion
def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        # si un movimiento lleva a que la IA gane, es lo mejor que puede pasar, su recompensa es infinita
        return float('inf')
    elif check_win(1, minimax_board):
        #  si un movimiento hace que la IA pierda, es lo peor que puede pasar, recompensa negativa infinita
        return float('-inf')
    # si un movimiento hace que el tablero se llene sin que nadie gane, es un empate, movimiento neutral
    elif is_board_full(minimax_board):
        return 0
    
    #evalua lo que hace el oponente  llamando a la funcion de forma recursiva 
    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2         # simulando movimiento de la IA
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)       
        return best_score
    
        # luego pretende ser el jugador  (piensa coom yo: quiero minimizar la puntuacion para la IA, que hago?
        
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:    #simulando movimiento en posicion vacia
                    minimax_board[row][col] = 1     #simulando movimiento del oponente
                    score = minimax(minimax_board, depth + 1, True)     #llama la siguiente capa maximizando 
                    minimax_board[row][col] = 0         #deshace movimiento
                    best_score = min(score, best_score)       #guarda la peor puntuacion encontrada
                    # best_score = max(score,best_score)          #ME PERMITE GANAR
        return best_score


# decide que movimiento hacer en el juego actual, el valor del tablero
def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):       #probando en cada casilla
            if board[row][col] == 0:        
                board[row][col] = 2         # partes del tablero donde hay fichas de la IA
                score = minimax(board, 0, False)        #obtiene la puntuacion de la jugada simulada
                board[row][col] = 0                     #deshace
                if score > best_score:     #comparando puntuacion de esa jugada con la mejor hallada hasta el momento
                    best_score = score      #si es mejor, guarda esa jugada como la mejor jugada candidata
                    move = (row, col)       #posicion real de la jugada (el movimiento que es la mejor opcion)


    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False


#logica del juego - verificando las celdas en las que se hicieron click
def restart_game():
     screen.fill(DARK)
     draw_lines()
     for row in range(BOARD_ROWS):
         for col in range(BOARD_COLS):
             board[row][col] = 0


draw_lines()


player = 1
game_over = False



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX): 
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1     #cambio de jugador

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1     #cambio de jugador

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:     #reiniciar el juego
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_lines(GRAY)
            draw_figures(GRAY)

    pygame.display.update()

        
