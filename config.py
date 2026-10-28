from enum import Enum
from typing import Literal

from pygame import Surface
import pygame

# -[[ KONSTANTE ]]-
CAPTION = "Trouglići"
SCREEN_WIDTH: int = 900
SCREEN_HEIGHT: int = 800
SCREEN: Surface = None

PADDING: int = 50

PLAYABLE_AREA_WIDTH: int = SCREEN_WIDTH - 2 * PADDING
PLAYABLE_AREA_HEIGHT: int = SCREEN_HEIGHT - 2 * PADDING # ne uzima u obzir velicinu UI-a na vrhu;
PLAYABLE_AREA_DIMS: tuple[int, int] = (PLAYABLE_AREA_WIDTH, PLAYABLE_AREA_HEIGHT)

class DIRECTION(Enum):
    HORIZONTAL_RIGHT = "horizontal_right"
    HORIZONTAL_LEFT = "horizontal_left"
    DIAGONAL_UP_LEFT = "diagonal_up_left"
    DIAGONAL_UP_RIGHT = "diagonal_up_right"
    DIAGONAL_DOWN_LEFT = "diagonal_down_left"
    DIAGONAL_DOWN_RIGHT = "diagonal_down_right"

# -[[ PROMENLJIVE ]]-
ui_top_height: int = 0 # dinamicki se odredjuje prilikom iscrtavanja;

board_size: Literal[4, 5, 6, 7, 8] = None
board_rows_num: int = None # broj redova; zavisi od 'board_size'; takodje i broj pinova/kolona za red u sredini;
board_triangle_num: int = None # maks broj trouglova koji mogu da se formiraju; zavisi od 'board_size';
board_pin_to_pin_horizontal_distance: int = None # horizontalna udaljenost izmedju dva pina u istom redu
board_pin_to_next_row_vertical_distance: int = None # vertikalna udaljenost pina do sledeceg reda; pinovi nisu jedan ispod drugog pa ne moze pin_to_pin

board_random_state_max_turns: int = 100 # nasumicno stanje moze imati maks 100 poteza

show_indexes: bool = False # da li se indeksi iscrtavaju iznad pinova; npr. A1

show_possible_states = False
possible_state_ind = 0
all_possible_states = []

key_processed = {
    pygame.K_u: False,
    pygame.K_i: False,
}

# AI Konfiguracija
AI_SEARCH_DEPTH = 2 # Dubina pretrage Minimax algoritma 3    
AI_PLAYER='O'