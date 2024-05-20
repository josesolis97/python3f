import random
import numpy as np
import pygame
import sys
import math

# Definimos filas y columnas
FILA = 6
COLUMNA = 8

# Definimos colores
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
MORADO = (128, 0, 128)
NARANJA = (255, 165, 0)
CIAN = (0, 255, 255)
ROSADO = (255, 192, 203)
MARRON = (139, 69, 19)

# Diccionario para asociar los nombres de los colores con los valores RGB
colores_disponibles = {
    "AZUL": AZUL,
    "NEGRO": NEGRO,
    "AMARILLO": AMARILLO,
    "ROJO": ROJO,
    "VERDE": VERDE,
    "BLANCO": BLANCO,
    "MORADO": MORADO,
    "NARANJA": NARANJA,
    "CIAN": CIAN,
    "ROSADO": ROSADO,
    "MARRON": MARRON
}

# Función para obtener un color válido del jugador
def obtener_color(jugador):
    color = input(jugador + " ingrese el Color: ").upper()
    while color not in colores_disponibles:
        print("Color no válido. Intente nuevamente.")
        color = input(jugador + " ingrese el Color: ").upper()
    return colores_disponibles[color]

# Función para obtener si el oponente es la computadora
def es_computadora(jugador):
    respuesta = input(jugador + " desea jugar contra la computadora? (S/N): ").upper()
    return respuesta == 'S'

# Selección de colores para el jugador 1
jugador1 = input("Ingrese el nombre del jugador 1: ").upper()
color1 = obtener_color(jugador1)

# Selección de oponente
computadora = es_computadora(jugador1)

if computadora:
    jugador2 = "COMPUTADORA"
    color2 = random.choice(list(colores_disponibles.values()))
else:
    jugador2 = input("Ingrese el nombre del jugador 2: ").upper()
    color2 = obtener_color(jugador2)

# Seteamos una fuente
pygame.font.init()
MY_FUENTE = pygame.font.SysFont("monospace", 75) 

# Definimos ancho y alto
TAMANIOCAJA = 100
ancho = COLUMNA * TAMANIOCAJA
alto = (FILA+1) * TAMANIOCAJA

tamanio = (ancho, alto)
# Definimos circunferencia
RADIO = int(TAMANIOCAJA/2 - 5)

def crear_tablero():
    board = np.zeros((FILA, COLUMNA))
    return board

def lugar_valida(board, col):
    return board[FILA-1][col] == 0

def obtener_siguiente_fila_disponible(board, col):
    for r in range(FILA):
        if board[r][col] == 0:
            return r

def soltar_pieza(board, row, col, piece):
    board[row][col] = piece

def mostrar_tablero(board):
    print(np.flipud(board))

def es_ganador(board, piece):
    # Revisando las posiciones horizontales
    for c in range(COLUMNA-3):
        for r in range(FILA):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    # Verificando las posiciones verticales
    for c in range(COLUMNA):
        for r in range(FILA-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Verificando diagonales positivas
    for c in range(COLUMNA-3):
        for r in range(FILA-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True 

    # Verificando diagonales negativas
    for c in range(COLUMNA-3):
        for r in range(3, FILA):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True 

def dibujar_tablero(board):
    for c in range(COLUMNA):
        for f in range(FILA):
            pygame.draw.rect(pantalla, AZUL, (c*TAMANIOCAJA, f*TAMANIOCAJA+TAMANIOCAJA, TAMANIOCAJA, TAMANIOCAJA))
            pygame.draw.circle(pantalla, NEGRO, (int(c*TAMANIOCAJA+TAMANIOCAJA/2), int(f*TAMANIOCAJA+TAMANIOCAJA+TAMANIOCAJA/2)), RADIO)

    for c in range(COLUMNA):
        for f in range(FILA):
            if board[f][c] == 1:
                pygame.draw.circle(pantalla, color1, (int(c*TAMANIOCAJA+TAMANIOCAJA/2), (alto+TAMANIOCAJA)-int(f*TAMANIOCAJA+TAMANIOCAJA+TAMANIOCAJA/2)), RADIO)
            elif board[f][c] == 2:
                pygame.draw.circle(pantalla, color2, (int(c*TAMANIOCAJA+TAMANIOCAJA/2), (alto+TAMANIOCAJA)-int(f*TAMANIOCAJA+TAMANIOCAJA+TAMANIOCAJA/2)), RADIO)
    
    pygame.display.update()

def obtener_movimiento_ia(board):
    movimientos_validos = [col for col in range(COLUMNA) if lugar_valida(board, col)]
    return random.choice(movimientos_validos)

tablero = crear_tablero()
game_over = False
turno = 0 # Variable para definir usuario 1 y 2

# Iniciamos pygame
pygame.init()
# Definimos nuestra pantalla
pantalla = pygame.display.set_mode(tamanio)
dibujar_tablero(tablero)

while not game_over:
    # Con esto evitamos que la pantalla se nos cierre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(pantalla, NEGRO, (0, 0, ancho, TAMANIOCAJA))
            posx = event.pos[0]
            if turno == 0:
                pygame.draw.circle(pantalla, color1, (posx, int(TAMANIOCAJA/2)), RADIO)
            else:
                pygame.draw.circle(pantalla, color2, (posx, int(TAMANIOCAJA/2)), RADIO)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(pantalla, NEGRO, (0, 0, ancho, TAMANIOCAJA))

            if turno == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/TAMANIOCAJA))

                if lugar_valida(tablero, col):
                    row = obtener_siguiente_fila_disponible(tablero, col)
                    soltar_pieza(tablero, row, col, 1)

                    if es_ganador(tablero, 1):
                        label = MY_FUENTE.render(jugador1 + " Gana!!!", 1, VERDE)
                        pantalla.blit(label, (40, 10))
                        game_over = True
            else:
                if computadora:
                    col = obtener_movimiento_ia(tablero)
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx/TAMANIOCAJA))

                if lugar_valida(tablero, col):
                    row = obtener_siguiente_fila_disponible(tablero, col)
                    soltar_pieza(tablero, row, col, 2)

                    if es_ganador(tablero, 2):
                        label = MY_FUENTE.render(jugador2 + " Gana!!!", 1, VERDE)
                        pantalla.blit(label, (40, 10))
                        game_over = True

            dibujar_tablero(tablero)

            turno += 1 
            turno = turno % 2

            if game_over:
                pygame.time.wait(3000)
