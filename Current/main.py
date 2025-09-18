import sys
import pygame
import numpy as np


pygame.init()


#Colores
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


#PROPORCIONES Y TAMANIOS
WIDTH = 300
HEIGHT = 300
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
screen.fill(BLACK)


#este campo esta vacio y no esta usado
board = np.zeros((BOARD_ROWS, BOARD_COLS))


#para colorear el tablero cuando gane, pierda o empate. Dibuja una linea con un color desde-hasta
def draw_lines(color=WHITE):
    for i in range (1, BOARD_ROWS):
        # pygame.draw.line(screen, color, start_pos:(0, SQUARE_SIZE * i), end_pos:(WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        # pygame.draw.line(screen, color, start_pos:(SQUARE_SIZE * i, 0), end_pos:(SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)
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
                                (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4))
                
                pygame.draw.line(screen, color, 
                                #  start_pos:
                                (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4 ),
                                #  end_pos:
                                (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4))
                

#tomando row y col del tablero, para establecer player en un espacio 
def mark_square(row, col, player):
    board[row][col] = player


#revisar si el espacio esta vacio
def available_square(row, col):
    return board[row][col] == 0


#tablero ficticio - futuro: aqui revisamos en el tablero presente si hay espacios vacios 
    #(por defecto sera el tablero presente pero no siempre sera asi)
def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return True
        return False


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