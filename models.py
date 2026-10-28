from itertools import pairwise
from typing import Literal
import pygame

# ==========================================================================================================================================
# ==========================================================================================================================================
# ==========================================================================================================================================

class Pin:
    """Predstavlja stubić na tabli."""
    PIN_RADIUS = 8
    PIN_COLOR = (255, 255, 255)
    PIN_INDEX_FONT_SIZE = 24

    def __init__(self, x: int, y: int, row_index: str, col_index: int):
        self.x = x
        self.y = y
        self.row_index = row_index
        self.col_index = col_index
        self.connections = set()  # Lista pinova sa kojima je trenutni pin povezan
        self.bounding_box = (x - Pin.PIN_RADIUS, y - Pin.PIN_RADIUS, 2 * Pin.PIN_RADIUS, 2 * Pin.PIN_RADIUS)

    def add_connection(self, pin: 'Pin'):
        """Povezuje trenutni pin sa pin-om navedenim kao argumetn, bitno za proveru trouglova."""
        if pin not in self.connections:
            self.connections.add(pin)
    
    def clear_connections(self):
        self.connections.clear()

    def draw(self, screen: pygame.Surface, show_indexes: bool):
        """Crta stubić na ekranu."""
        pygame.draw.circle(screen, Pin.PIN_COLOR, (self.x, self.y), 5)

        if show_indexes:  # Ispisuje indeks iznad stubića, uključuje/isključuje se sa pritiskom na slovo T
            font = pygame.font.Font(None, Pin.PIN_INDEX_FONT_SIZE)
            text = f"{self.row_index}{self.col_index}"
            text_surface = font.render(text, True, Pin.PIN_COLOR)
            text_rect = text_surface.get_rect(center=(self.x, self.y - 15))
            screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos: tuple[int, int]):
        """Proverava da li je igrač kliknuo na stubić."""
        bx, by, width, height = self.bounding_box
        return (bx <= mouse_pos[0] <= bx + width) and (by <= mouse_pos[1] <= by + height)
    
    def __hash__(self):
        return hash((self.row_index, self.col_index))
    
    def __eq__(self, other):
        if not isinstance(other, Pin):
            return False
        return (self.row_index == other.row_index and self.col_index == other.col_index)


# -------------------------------------------------------------------

class Rubber:
    """Predstavlja gumicu koja se postavlja između dva stubića."""

    def __init__(self, start_pin: Pin, end_pin: Pin):
        self.start_pin = start_pin
        self.end_pin = end_pin

    def draw(self, screen: pygame.Surface):
        pygame.draw.line(screen, (255, 0, 0), (self.start_pin.x, self.start_pin.y), (self.end_pin.x, self.end_pin.y), 3)


# -------------------------------------------------------------------

class Token:
    """Predstavlja oznaku igrača koja se postavlja unutar trouglova (ime token je uzeto sa sajta sa pravilima)."""
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)

    def __init__(self, pin1: Pin, pin2: Pin, pin3: Pin, player_label: str):
        self.pins = frozenset({pin1, pin2, pin3})
        self.player = player_label  # 'X' ili 'O'
        self.color = Token.GREEN if (player_label == Game.PLAYER_X) else Token.ORANGE

        # Središte trougla
        self.Cx = (pin1.x + pin2.x + pin3.x) / 3
        self.Cy = (pin1.y + pin2.y + pin3.y) / 3

    def draw(self, screen: pygame.Surface):
        font = pygame.font.Font(None, 36)

        text = font.render(self.player, True, self.color)

        text_rect = text.get_rect(center=(self.Cx, self.Cy))

        screen.blit(text, text_rect)
    
    def __hash__(self):
        return hash(self.pins)
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.pins == other.pins

# ==========================================================================================================================================
# ==========================================================================================================================================
# ==========================================================================================================================================

class Game:

    PLAYER_X: str = 'X'
    PLAYER_O: str = 'O'
    GAME_TIE: str = "Nerešeno"
    TOKEN_NUM_TAG: str = "stubić"

    def __init__(self):
        self.pins: dict[Pin] = {}
        self.selected_pin: Pin = None
        self.possible_paths: dict[Pin] = {}
        self.placed_rubbers: list[Rubber] = []
        self.placed_tokens: set[Token] = set()

        self.random_state: bool = False
        self.game_over: bool = False

        self.x_token_num: int = 0
        self.o_token_num: int = 0

        self.winning_token_num: int = -1
        self.winner: str = Game.GAME_TIE

        self.game_mode: Literal['Protiv kompjutera', 'Protiv drugog igraca'] | None = None
        self.current_player: Literal['X', 'O'] | None = None

    def reset(self):
        for pin in self.pins.values():
            pin.clear_connections()
        self.selected_pin = None
        self.possible_paths.clear()
        self.placed_rubbers.clear()
        self.placed_tokens.clear()
        self.random_state = False
        self.game_over = False
        self.x_token_num = 0
        self.o_token_num = 0
        self.winning_token_num = -1
        self.winner = Game.GAME_TIE

        self.last_move_data = None
        
    
    def swap_current_player(self):
        self.current_player = Game.PLAYER_O if self.current_player == Game.PLAYER_X else Game.PLAYER_X
    
    def increment_player_token_num(self, new_tokens_num: int):
        if self.current_player == Game.PLAYER_X:
            self.x_token_num += new_tokens_num
        else:
            self.o_token_num += new_tokens_num
    
    def deselect_pin(self):
        self.selected_pin = None
        self.possible_paths.clear()
    
    def deepcopy(original_game: "Game") -> "Game":
        new_game: Game = Game()
        
        new_game.game_over = original_game.game_over
        new_game.x_token_num = original_game.x_token_num
        new_game.o_token_num = original_game.o_token_num
        new_game.winning_token_num = original_game.winning_token_num
        new_game.winner = original_game.winner
        new_game.game_mode = original_game.game_mode
        new_game.current_player = original_game.current_player
        

        for _, og_pin in original_game.pins.items():
            new_game_pin = Pin(
                og_pin.x,
                og_pin.y,
                og_pin.row_index,
                og_pin.col_index
            )
            new_game.pins[(new_game_pin.row_index, new_game_pin.col_index)] = new_game_pin
        
        for og_pin_id, og_pin in original_game.pins.items():
            new_game.pins[og_pin_id].connections = {new_game.pins[(og_pin_con.row_index, og_pin_con.col_index)] for og_pin_con in og_pin.connections}
        
        new_game.placed_tokens = {
            Token(
                *[new_game.pins[(pin.row_index, pin.col_index)] for pin in og_token.pins],
                og_token.player
            )
            for og_token in original_game.placed_tokens
        }

        # samo za testiranje, nije bitno kasnije za AI protivnika jer samo trosi memoriju bzvz
        new_game.placed_rubbers = [
            Rubber(new_game.pins[(og_rubber.start_pin.row_index, og_rubber.start_pin.col_index)],
                   new_game.pins[(og_rubber.end_pin.row_index, og_rubber.end_pin.col_index)])
            for og_rubber in original_game.placed_rubbers
        ]
        
        return new_game


    def apply_move(self, path: list[Pin]) -> dict:
        move_data = {
            "path": path.copy(),
            "connected_pairs": [],
            "rubbers": [],
            "new_tokens": [],
        }

        for current_pin, next_pin in pairwise(path):
            if next_pin not in current_pin.connections:
                current_pin.add_connection(next_pin)
                next_pin.add_connection(current_pin)
                move_data["connected_pairs"].append((current_pin, next_pin))

            rubber = Rubber(current_pin, next_pin)
            self.placed_rubbers.append(rubber)
            move_data["rubbers"].append(rubber)

        for current_pin, next_pin in pairwise(path):
            common_pins = (current_pin.connections & next_pin.connections) - {current_pin, next_pin}

            for common_pin in common_pins:
                new_token = Token(current_pin, next_pin, common_pin, self.current_player)
                if new_token not in self.placed_tokens:
                    self.placed_tokens.add(new_token)
                    move_data["new_tokens"].append(new_token)

        self.increment_player_token_num(len(move_data["new_tokens"]))

        return move_data

    def undo_move(self, move_data: dict):
        for token in move_data["new_tokens"]:
            self.placed_tokens.discard(token)

        if self.current_player == Game.PLAYER_X:
            self.x_token_num -= len(move_data["new_tokens"])
        else:
            self.o_token_num -= len(move_data["new_tokens"])

        for rubber in move_data["rubbers"]:
            if rubber in self.placed_rubbers:
                self.placed_rubbers.remove(rubber)

        for pin_a, pin_b in move_data["connected_pairs"]:
            pin_a.connections.discard(pin_b)
            pin_b.connections.discard(pin_a)


