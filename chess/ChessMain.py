"""
Edit Coding and Update by: xMeiker
Archivo del controlador principal.
Manejo de la entrada del usuario.
Mostrando el objeto GameStatus actual.
"""
import pygame as p
import ChessEngine, ChessAI, ChessMenu
import sys
from multiprocessing import Process, Queue

#Nombre del proyecto e icono
p.display.set_caption('Chess With AI')
title = p.image.load('images/title.png')
p.display.set_icon(title)

#Variables globales
BOARD_WIDTH = BOARD_HEIGHT = 512
MOV_PANEL_WIDTH = 250
MOV_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def main():
    # Llamando a la clase del menu principal del juego
    menuInicio()

def menuInicio():
    # Llama a la clase donde se encuentra la interfaz del menu de inicio
    menu = ChessMenu.Menu()
    menu.run()

def loadImages():
    """
    Inicializa un directorio global de IMAGENES.
    Esto se llamará exactamente una vez en el archivo principal.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def Inicio():
    """
        El controlador principal de nuestro código.
        Esto manejará la entrada del usuario y la actualización de los gráficos.
        """
    #Nombre
    p.display.set_caption('Chess With AI')
    # Inicializa los procesos del Chess
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOV_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # variable de bandera para cuando se realiza un movimiento
    animate = False  # variable de bandera para cuando debemos animar un movimiento
    loadImages()  # haz esto solo una vez antes del bucle while
    running = True
    square_selected = ()  # inicialmente no se selecciona ningún cuadrado, esto realizará un seguimiento del último clic del usuario (tupla (fila, columna))
    player_clicks = []  # esto realizará un seguimiento de los clics del jugador (dos tuplas)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = True  # Si un humano juega con las blancas, entonces esto será Verdadero; de lo contrario, Falso.
    player_two = False  # Si un humano juega con las negras, entonces esto será Verdadero; de lo contrario, Falso.

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # Controlador de mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) ubicación del ratón
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (
                    row, col) or col >= 8:  # El usuario hizo clic en el mismo cuadrado dos veces.
                        square_selected = ()  # deseleccionar
                        player_clicks = []  # borrar clics
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # agregar para el primer y segundo clic
                    if len(player_clicks) == 2 and human_turn:  # después del segundo clic
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # restablecer clics de usuario
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            # Manipulador de llaves
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # deshacer cuando se presiona 'z'
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # reiniciar el juego cuando se presiona 'r'
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # Buscador de movimientos IA
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # utilizado para pasar datos entre hilos
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ChessAI.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animatorLog(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawStateGame(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMovLog(screen, game_state, move_log_font)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawTextEndGame(screen, "Las negras ganan por jaque mate")
            else:
                drawTextEndGame(screen, "Las blancas ganan por jaque mate")

        elif game_state.stalemate:
            game_over = True
            drawTextEndGame(screen, "Estancado")

        clock.tick(MAX_FPS)
        p.display.flip()

def drawStateGame(screen, game_state, valid_moves, square_selected):
    """
    Responsable de todos los gráficos dentro del estado actual del juego.
    """
    drawBoard(screen)  # dibujar cuadrados en el tablero
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # dibuja piezas encima de esos cuadrados

def drawBoard(screen):
    """
    Dibuja los cuadrados en el tablero.
    El cuadrado superior izquierdo siempre es claro.
    """
    global colors
    colors = [p.Color("papayawhip"), p.Color("tan")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Resalta el cuadrado seleccionado y mueve la pieza seleccionada.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected es una pieza que se puede mover
            # resaltar el cuadrado seleccionado
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # Valor de transparencia 0 -> transparente, 255 -> opaco
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # resaltar movimientos de ese cuadrado
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

def drawPieces(screen, board):
    """
    Dibuja las piezas en el tablero usando el game_state.board actual.
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawMovLog(screen, game_state, font):
    """
    Dibuja el registro de movimientos.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOV_PANEL_WIDTH, MOV_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('gray'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('black'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

def drawTextEndGame(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))

def animatorLog(move, screen, board, clock):
    """
    Animando un movimiento
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # marcos para mover un cuadrado
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # borrar la pieza movida desde su casilla final
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # dibujar la pieza capturada en un rectángulo
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # dibujar pieza en movimiento
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
