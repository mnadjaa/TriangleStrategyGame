from itertools import pairwise
import random

from config import DIRECTION
from models import *
import config


# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# BOARD CREATION
# ██████   ██████   █████  ██████  ██████       ██████ ██████  ███████  █████  ████████ ██  ██████  ███    ██ 
# ██   ██ ██    ██ ██   ██ ██   ██ ██   ██     ██      ██   ██ ██      ██   ██    ██    ██ ██    ██ ████   ██ 
# ██████  ██    ██ ███████ ██████  ██   ██     ██      ██████  █████   ███████    ██    ██ ██    ██ ██ ██  ██ 
# ██   ██ ██    ██ ██   ██ ██   ██ ██   ██     ██      ██   ██ ██      ██   ██    ██    ██ ██    ██ ██  ██ ██ 
# ██████   ██████  ██   ██ ██   ██ ██████       ██████ ██   ██ ███████ ██   ██    ██    ██  ██████  ██   ████ 


def create_board(board_size: int, playable_area_dims: tuple[int, int], ui_top_height: int, padding: int):
    """Kreira tablu na kojoj se igra."""
    pins = {}

    # Vertikalna udaljenost između stubića
    total_rows = board_size * 2 - 1
    vertical_spacing = (playable_area_dims[1]-ui_top_height) / (total_rows - 1)

    # Horizontalna udaljenost
    max_pins_in_one_row = board_size * 2 - 1  # broj stubića u središnjem redu jer on ima najviše
    horizontal_spacing = playable_area_dims[0] / (max_pins_in_one_row - 1)

    row_labels = [chr(ord('A') + i) for i in range(total_rows)]  # A, B, C...

    for row in range(total_rows):
        if row < board_size:
            pin_count = board_size + row
        else:
            pin_count = board_size * 2 - 2 - (row - board_size)

        # offset za centriranje reda
        row_offset = (max_pins_in_one_row - pin_count) * horizontal_spacing / 2

        # Postavljanje stubića sa odgovarajućim koordinatama
        for col in range(pin_count):
            x = padding + row_offset + col * horizontal_spacing
            y = padding + ui_top_height + row * vertical_spacing
            pin = Pin(int(x), int(y), row_labels[row], col + 1)
            pins[(row_labels[row], col+1)] = pin # kljuc je npr. A1 u formatu (row, col) <- obavezne 2 zagrade prilikom zvanja jer je to jedan kljuc: pins( (row, col) )

    return pins
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================


# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# CLICK DETECTION
#  ██████ ██      ██  ██████ ██   ██     ██████  ███████ ████████ ███████  ██████ ████████ ██  ██████  ███    ██ 
# ██      ██      ██ ██      ██  ██      ██   ██ ██         ██    ██      ██         ██    ██ ██    ██ ████   ██ 
# ██      ██      ██ ██      █████       ██   ██ █████      ██    █████   ██         ██    ██ ██    ██ ██ ██  ██ 
# ██      ██      ██ ██      ██  ██      ██   ██ ██         ██    ██      ██         ██    ██ ██    ██ ██  ██ ██ 
#  ██████ ███████ ██  ██████ ██   ██     ██████  ███████    ██    ███████  ██████    ██    ██  ██████  ██   ████ 


def get_clicked_pin_area(mouse_pos: tuple[int, int], board_size: int, board_rows_num: int, playable_area_dims: tuple[int,int],
                         ui_top_height: int, pin_area_width: int, pin_area_height: int, pin_area_row_margin: int, padding: int):
    board_top_left = (0, padding)

    if not (board_top_left[0] <= mouse_pos[0] <= board_top_left[0] + playable_area_dims[0] + padding*2 and
            board_top_left[1] <= mouse_pos[1] <= board_top_left[1] + playable_area_dims[1] + ui_top_height):
        # print("Izvan")
        return None  # kliknuto van

    # odredjivanje na koji red je kliknuto
    y_offset = mouse_pos[1] - board_top_left[1]
    clicked_row = int(y_offset // (pin_area_height + pin_area_row_margin - padding))

    if y_offset % (pin_area_height + pin_area_row_margin - padding) >= pin_area_height:
        return None  # kliknuto negde izmedju redova

    # odredjivanje koliko pinova ima na kliknutom redu
    if clicked_row < board_size:
        clicked_row_length = board_size + clicked_row # kliknuto na red pre srednjeg reda
    else:
        clicked_row_length = board_size + (board_rows_num - 1 - clicked_row) # kliknuto na red posle srednjeg reda

    clicked_row_offset = (playable_area_dims[0] - clicked_row_length * pin_area_width + padding*2) // 2
    x_offset = mouse_pos[0] - board_top_left[0] - clicked_row_offset

    if x_offset < 0 or x_offset >= clicked_row_length * pin_area_width:
        return None  # kliknuto izmedju kolona reda

    row_letter = chr(clicked_row + ord('A'))
    col_number = int(x_offset // pin_area_width) + 1

    # print(f"Kliknuto na oblast: {row_letter}{col_number}")

    return (row_letter, col_number)
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================


# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# PATH FORMING
# ██████   █████  ████████ ██   ██     ███████  ██████  ██████  ███    ███ ██ ███    ██  ██████  
# ██   ██ ██   ██    ██    ██   ██     ██      ██    ██ ██   ██ ████  ████ ██ ████   ██ ██       
# ██████  ███████    ██    ███████     █████   ██    ██ ██████  ██ ████ ██ ██ ██ ██  ██ ██   ███ 
# ██      ██   ██    ██    ██   ██     ██      ██    ██ ██   ██ ██  ██  ██ ██ ██  ██ ██ ██    ██ 
# ██      ██   ██    ██    ██   ██     ██       ██████  ██   ██ ██      ██ ██ ██   ████  ██████  


def form_directed_path_from_pin(start_pin: Pin, direction: DIRECTION, pins: dict[Pin], board_size: int):
    """
    Izračunava pravilan put od 4 stubića u datom smeru 'direction' počevši od start_pin-a
    Ukoliko odgovarajući put ne postoji, vraća prazan niz.
    """
    
    WANTED_PATH_LENGTH = 4 # put mora da sadrži tačno 4 stubića
    MIDDLE_ROW = board_size - 1  # indeks središnjeg reda (0-based)

    potential_path = [start_pin]

    current_row = ord(start_pin.row_index) - ord('A')  # indeks trenutnog reda (0-based)
    current_col = start_pin.col_index  # indeks trenutne kolone
#________________________________________________________________________________________________
    for _ in range(WANTED_PATH_LENGTH-1):  # počevši od start_pin-a, treba nam još 3 stubića
        if direction == DIRECTION.DIAGONAL_UP_RIGHT:
            if current_row > MIDDLE_ROW:  # donja polovina table
                current_row -= 1  # pomeramo se na gore
                if current_row >= MIDDLE_ROW:
                    current_col += 1
            else:  # gornja polovina table ili red u sredini table
                current_row -= 1
                # nema potrebe da menjamo indeks kolone

        elif direction == DIRECTION.DIAGONAL_UP_LEFT:
            if current_row >= MIDDLE_ROW:  # donja polovina table (sa redom u sredini)
                current_row -= 1
                if current_row < MIDDLE_ROW:  # ukoliko prelazimo u gornju polovinu
                    current_col -= 1
            else:  # gornja polovina table
                current_row -= 1
                current_col -= 1

        elif direction == DIRECTION.DIAGONAL_DOWN_LEFT:
            current_row += 1  # uvek se inkrementira
            if current_row <= MIDDLE_ROW:  # gornja polovina (sa redom u sredini)
                pass  # indeks kolone se ne menja
            else:  # donja polovina
                current_col -= 1

        elif direction == DIRECTION.DIAGONAL_DOWN_RIGHT:
            current_row += 1  # uvek se inkrementira
            if current_row <= MIDDLE_ROW:  # gornja polovina (sa redom u sredini)
                current_col += 1
            else:  # donja polovina table
                pass

        elif direction == DIRECTION.HORIZONTAL_RIGHT:
            current_col += 1

        elif direction == DIRECTION.HORIZONTAL_LEFT:
            current_col -= 1

        # konverzija nazad u slovni indeks za redove
        new_row = chr(current_row + ord('A'))
        new_col = current_col

        next_pin = pins.get((new_row, new_col))
        if not next_pin:
            return []  # izlazi se sa table

        potential_path.append(next_pin)
#________________________________________________________________________________________________

    if len(potential_path) != WANTED_PATH_LENGTH:
        return []

    # provera da li je put vec povezan
    for current_pin, next_pin in pairwise(potential_path):
        if next_pin not in current_pin.connections:
            return potential_path # barem dva pina nisu direktno povezana, vraca se potencijalni put
        
    return []  # Svi pinovi su povezani -> vraćamo []


# =====================================================================================================


def form_directed_path_from_pin_to_pin(start_pin: Pin, end_pin: Pin, direction: DIRECTION, pins: dict[Pin], board_size: int):
    path = form_directed_path_from_pin(start_pin, direction, pins, board_size)

    if path and (path[-1] == end_pin):
        #_print_directed_path(start_pin, end_pin, path)
        return path
    else:
        return None


def _print_directed_path(start_pin: Pin, end_pin: Pin, path: list[Pin]) -> None:
    print("\n╔══════════════════════════════════════════╗")
    print(f"║ → Put od [{start_pin.row_index}{start_pin.col_index}] do [{end_pin.row_index}{end_pin.col_index}]:                   ║")
    
    path_str = "║          "
    for i, pin in enumerate(path):
        if i == len(path) - 1:
            path_str += f" {pin.row_index}{pin.col_index}"
        else:
            path_str += f" {pin.row_index}{pin.col_index} →"
    path_str += "              ║"
    print(path_str)

    print("╚══════════════════════════════════════════╝\n")


# =====================================================================================================


def form_all_possible_paths_from_pin(start_pin: Pin, pins: dict[Pin], board_size: int):
    """Funkcija koja na osnovu zadatog stanje igre (table) i početnog selektovanog pina formira sve moguće poteze za trenutnog igrača.
    Vraća dictionary gde je ključ odredišni pin, a vrednost je tuple (smer, put)."""
    
    paths_with_directions = {
        path[-1]: (direction, path)
        for direction in DIRECTION
        if (path := form_directed_path_from_pin(start_pin, direction, pins, board_size))
    }
    
    return paths_with_directions


# =====================================================================================================


def form_all_possible_paths(pins: dict[Pin], board_size: int) -> dict[Pin, dict[Pin, DIRECTION]]:
    """Formira sve moguće poteze za trenutnog igrača na potezu
     - Ne uzima u obzir duplikate (poteze koji formiraju isti put)"""
    
    all_possible_paths = {}
    added_paths = set()

    for start_pin in pins.values():
        pin_paths = form_all_possible_paths_from_pin(start_pin, pins, board_size)
        end_pins = {}

        for end_pin, (direction,_) in pin_paths.items():
            pair_key = frozenset({start_pin, end_pin})

            if pair_key not in added_paths:
                added_paths.add(pair_key)
                end_pins[end_pin] = direction

        if end_pins:
            all_possible_paths[start_pin] = end_pins

    #_print_all_possible_paths(all_possible_paths)
    return all_possible_paths

def _print_all_possible_paths(all_possible_paths: dict[Pin, dict[Pin, DIRECTION]]) -> None:
    print("\n╔══════════════════════════════════════════╗")
    print(  "║  SVI MOGUĆI POTEZI ZA TRENUTNOG IGRAČA:  ║")
    print(  "║             (bez duplikata)              ║")
    print(  "╚══════════════════════════════════════════╝\n")
    
    if not all_possible_paths:
        print("  Nema mogućih poteza!  ")
    else:
        for start_pin, end_pin_map in all_possible_paths.items():
            start_str = f"{start_pin.row_index}{start_pin.col_index}"
            print(f"[{start_str}]")
            end_items = list(end_pin_map.items())
            for i, (end_pin, direction) in enumerate(end_items):
                end_str = f"{end_pin.row_index}{end_pin.col_index}"
                arrow = "└─>" if i == len(end_items) - 1 else "├─>"
                print(f"  {arrow} [{end_str}] ({direction.value})")
            if end_items:
                print("")
    
    print( "╔══════════════════════════════════════════╗")
    print( "║    x   svi mogući potezi ispisani   x    ║")
    print( "╚══════════════════════════════════════════╝\n")


# =====================================================================================================


def apply_all_possible_paths(original_game: Game, all_possible_paths: dict[Pin, dict[Pin, DIRECTION]], board_size: int) -> list[Game]:
    new_games = []
    
    for start_pin, end_pins_dict in all_possible_paths.items():
        for end_pin, direction in end_pins_dict.items():
            new_game = Game.deepcopy(original_game)
            
            path = form_directed_path_from_pin_to_pin(
                new_game.pins[(start_pin.row_index, start_pin.col_index)], 
                new_game.pins[(end_pin.row_index, end_pin.col_index)],
                direction, 
                new_game.pins, 
                board_size
            )
            
            if path:
                new_game.placed_rubbers.append(Rubber(path[0], path[-1]))
                connect_pins_and_check_for_triangles(new_game, path)

                new_game.swap_current_player()
                
                new_games.append(new_game)
    
    return new_games
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================


# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# MOVE LOGIC
# ███    ███  ██████  ██    ██ ███████     ██       ██████   ██████  ██  ██████ 
# ████  ████ ██    ██ ██    ██ ██          ██      ██    ██ ██       ██ ██      
# ██ ████ ██ ██    ██ ██    ██ █████       ██      ██    ██ ██   ███ ██ ██      
# ██  ██  ██ ██    ██  ██  ██  ██          ██      ██    ██ ██    ██ ██ ██      
# ██      ██  ██████    ████   ███████     ███████  ██████   ██████  ██  ██████ 


def connect_pins_and_check_for_triangles(game: Game, path: list[Pin]):
    """Funkcija koja na osnovu zadatog mogućeg puta ('path' prethodno izabran iz liste mogućih) i zadatog stanja igre formira novo stanje igre"""

    newly_formed_triangles_num = 0  # Brojač novonastalih trouglova za trenutnog igrača gde postavlja tokene/stubice posle

    # Povezivanje pinova
    for current_pin, next_pin in pairwise(path):
        current_pin.add_connection(next_pin)
        next_pin.add_connection(current_pin)

    # Provera da li su nastali ili vec postoje trouglovi oko novopostavljene gumice
    for current_pin, next_pin in pairwise(path):
        common_pins = (current_pin.connections & next_pin.connections) - {current_pin, next_pin} # zajednicki pinovi sa kojima su povezana dva susedna pina puta

        # Dodavanje novih tokena
        for common_pin in common_pins:
            new_token = Token(current_pin, next_pin, common_pin, game.current_player)
            if new_token not in game.placed_tokens:
                game.placed_tokens.add(new_token)
                newly_formed_triangles_num += 1
    
    game.increment_player_token_num(newly_formed_triangles_num)


# =====================================================================================================


def calculate_total_triangles_num(size: int):
    """Računa ukupan broj trouglova koje je moguće napraviti postavljanjem gumicama"""
    rows = list(range(size, 2 * size)) + list(range(2 * size - 2, size - 1, -1)) # racuna duzine redova

    total_triangles = 0

    for i in range(len(rows) - 1):
        # logika je da broj trouglova izmedju svaka dva susedna reda stubica iznosi duzina_prvog_reda + duzina_drugog_reda - 2
        total_triangles += rows[i] + rows[i + 1] - 2

    return total_triangles


# =====================================================================================================


def check_for_game_end(game: Game, board_triangle_num: int):
    """Proverava da li se došlo do ***kraja*** igre."""
    if game.x_token_num >= board_triangle_num / 2 + 1:
        game.game_over = True
        game.winner = Game.PLAYER_X
        game.winning_token_num = game.x_token_num
    elif game.o_token_num >= board_triangle_num / 2 + 1:
        game.game_over = True
        game.winner = Game.PLAYER_O
        game.winning_token_num = game.o_token_num
    elif game.x_token_num == board_triangle_num/2 and game.x_token_num == game.o_token_num:
        game.game_over = True
        game.winner = Game.GAME_TIE
        game.winning_token_num = -1
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================


# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# RANDOM STATE
# ██████   █████  ███    ██ ██████   ██████  ███    ███     ███████ ████████  █████  ████████ ███████ 
# ██   ██ ██   ██ ████   ██ ██   ██ ██    ██ ████  ████     ██         ██    ██   ██    ██    ██      
# ██████  ███████ ██ ██  ██ ██   ██ ██    ██ ██ ████ ██     ███████    ██    ███████    ██    █████   
# ██   ██ ██   ██ ██  ██ ██ ██   ██ ██    ██ ██  ██  ██          ██    ██    ██   ██    ██    ██      
# ██   ██ ██   ██ ██   ████ ██████   ██████  ██      ██     ███████    ██    ██   ██    ██    ███████ 


def create_random_state(game: Game, board_size: int, board_triangle_num: int, max_turns: int):
    """Postavlja igru u nasumično stanje, posle je moguće nastaviti igru od tog stanja"""
    game.reset()
    game.random_state = True

    autoplay_remaining_moves = random.randint(10, max_turns)

    game.game_over = False
    while autoplay_remaining_moves > 0:
            if game.game_over:
                autoplay_remaining_moves = 0
                break

            clicked_pin = list(game.pins.values())[random.randint(0, len(game.pins) - 1)]

            if clicked_pin:
                if game.selected_pin is None:
                    game.selected_pin = clicked_pin
                    possible_paths = form_all_possible_paths_from_pin(game.selected_pin, game.pins, board_size)
                    game.possible_paths = {end_pin: path for end_pin, (_, path) in possible_paths.items()}

                else:
                    if len(game.possible_paths) > 0:
                        random_path_index = random.randint(0, len(game.possible_paths) - 1)
                        possible_path = list(game.possible_paths.values())[random_path_index]
                        clicked_pin = possible_path[-1]

                        game.placed_rubbers.append(Rubber(possible_path[0], possible_path[-1]))

                        connect_pins_and_check_for_triangles(game, possible_path)

                        game.swap_current_player()

                        autoplay_remaining_moves -= 1

                        check_for_game_end(game, board_triangle_num)

                    game.deselect_pin()

    game.deselect_pin()
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================

# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
#      ___       __  
#     /   \     |  | 
#    /  ^  \    |  | 
#   /  /_\  \   |  | 
#  /  _____  \  |  | 
# /__/     \__\ |__| 

def evaluate_board_state(game: Game) -> float:
    ai_tokens = game.o_token_num
    opponent_tokens = game.x_token_num

    # Dodatni uslovi za pobedu/gubitak
    total_triangles = calculate_total_triangles_num(config.board_size)
    if game.game_over:
        if game.winner == Game.PLAYER_O:
            return float('inf') # AI pobedio, beskonačno dobra ocena
        elif game.winner != Game.GAME_TIE: # Protivnik pobedio
            return float('-inf') # AI izgubio, beskonačno loša ocena
        else: # Nerešeno
            return 0 # Nerešeno se vrednuje neutralno

    token_diff = ai_tokens - opponent_tokens
    progress_score = (ai_tokens / total_triangles) * 10  # Napredak prema cilju
    rubber_count_penalty = -len(game.placed_rubbers) * 0.1  # Penalizuj previše gumica

    return token_diff + progress_score + rubber_count_penalty



def minimax(game: Game, depth: int, maximizing_player: bool, alpha: float, beta: float):
    if depth == 0 or game.game_over:
        return evaluate_board_state(game)

    all_possible_moves = form_all_possible_paths(game.pins, config.board_size)

    if maximizing_player:
        max_eval = float('-inf')
        for start_pin, end_pins_dict in all_possible_moves.items():
            for end_pin, direction in end_pins_dict.items():
                path = form_directed_path_from_pin_to_pin(
                    game.pins[(start_pin.row_index, start_pin.col_index)],
                    game.pins[(end_pin.row_index, end_pin.col_index)],
                    direction,
                    game.pins,
                    config.board_size
                )
                if path:
                    move_data = game.apply_move(path)
                    eval = minimax(game, depth - 1, False, alpha, beta)
                    game.undo_move(move_data)

                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        print("odseceno je")
                        break
            if beta <= alpha:
                print("odseceno je")
                break
        return max_eval
    else:
        min_eval = float('inf')
        for start_pin, end_pins_dict in all_possible_moves.items():
            for end_pin, direction in end_pins_dict.items():
                path = form_directed_path_from_pin_to_pin(
                    game.pins[(start_pin.row_index, start_pin.col_index)],
                    game.pins[(end_pin.row_index, end_pin.col_index)],
                    direction,
                    game.pins,
                    config.board_size
                )
                if path:
                    move_data = game.apply_move(path)
                    eval = minimax(game, depth - 1, True, alpha, beta)
                    game.undo_move(move_data)

                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        print("odseceno je")
                        break
            if beta <= alpha:
                print("odseceno je")
                break
        return min_eval



def find_best_move(game: Game, depth: int) -> tuple[Pin, Pin, DIRECTION] | None:
    best_eval = float('-inf')
    best_move = None

    all_possible_moves = form_all_possible_paths(game.pins, config.board_size)

    if not all_possible_moves:
        return None

    for start_pin, end_pins_dict in all_possible_moves.items():
        for end_pin, direction in end_pins_dict.items():
            path = form_directed_path_from_pin_to_pin(
                game.pins[(start_pin.row_index, start_pin.col_index)],
                game.pins[(end_pin.row_index, end_pin.col_index)],
                direction,
                game.pins,
                config.board_size
            )
            if path:
                move_data = game.apply_move(path)
                eval = minimax(game, depth - 1, False, float('-inf'), float('inf'))
                game.undo_move(move_data)

                if eval > best_eval:
                    best_eval = eval
                    best_move = (start_pin, end_pin, direction)

    return best_move


def computers_turn(game: Game):
    print(f"AI razmišlja...")
    
    if len(game.placed_rubbers) == 0: # Tabla je prazna, kompjuter prvi igra neki random potez
        ai_start_pin = list(game.pins.values())[random.randint(0, len(game.pins) - 1)]
        game.selected_pin = ai_start_pin
        possible_paths = form_all_possible_paths_from_pin(game.selected_pin, game.pins, config.board_size)
        game.possible_paths = {ai_end_pin: path for ai_end_pin, (_, path) in possible_paths.items()}

        random_path_index = random.randint(0, len(game.possible_paths) - 1)
        possible_path = list(game.possible_paths.values())[random_path_index]

        game.placed_rubbers.append(Rubber(possible_path[0], possible_path[-1]))

        connect_pins_and_check_for_triangles(game, possible_path)

        game.swap_current_player()

        check_for_game_end(game, config.board_triangle_num)

        game.deselect_pin()

    else:
        ai_best_move = None
        ai_best_move = find_best_move(game, config.AI_SEARCH_DEPTH)
    
        if ai_best_move:
            ai_start_pin, ai_end_pin, ai_direction = ai_best_move
        
            # Moramo dobiti reference na Pin objekte iz trenutne 'game' instance
            ai_start_pin = game.pins[(ai_start_pin.row_index, ai_start_pin.col_index)]
            ai_end_pin = game.pins[(ai_end_pin.row_index, ai_end_pin.col_index)]
        
            # Rekreiranje putanje koristeći stvarne Pin objekte iz game.pins
            ai_path = form_directed_path_from_pin_to_pin(
                ai_start_pin, ai_end_pin, ai_direction, game.pins, config.board_size
            )
        
            if ai_path:
                game.placed_rubbers.append(Rubber(ai_path[0], ai_path[-1]))
                connect_pins_and_check_for_triangles(game, ai_path)
                game.swap_current_player()
                check_for_game_end(game, config.board_triangle_num)
            else:
                # Ovde nikada ne bi trebalo da se uđe
                print("AI je pokušao da odigra već zauzet potez ili nepostojeći.")
                game.swap_current_player() # Preskakanje poteza da se igra ne zaglavi
        else:
            # Ovde nikada ne bi trebalo da se uđe
            print("AI nema mogućih poteza. Verovatno je igra gotova ili je tabla puna.")
            game.game_over = True
            
    print(f"AI je odigrao svoj potez.")
        

# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================


def humans_turn(game: Game, sys):
    for event in pygame.event.get():
        # Zatvaranje prozora
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Kad je igra završena, nije više potrebno da se detektuju eventi
        if game.game_over:
            continue

        elif event.type == pygame.KEYDOWN:
            # Uključivanje/isključivanje prikaza indeksa iznad stubića (slovo t/T)
            if event.key == pygame.K_t:
                config.show_indexes = not config.show_indexes
            
            # samo test za apply_move i undo_move...
            if event.key == pygame.K_u and not config.key_processed[pygame.K_u]:
                t_path = [game.pins.get(('A', 1)), game.pins.get(('A', 2)), game.pins.get(('A', 3)), game.pins.get(('A', 4))]
                game.last_move_data = game.apply_move(t_path)
                config.key_processed[pygame.K_u] = True
                config.key_processed[pygame.K_i] = False

            if event.key == pygame.K_i and not config.key_processed[pygame.K_i]:
                game.undo_move(game.last_move_data)
                config.key_processed[pygame.K_i] = True
                config.key_processed[pygame.K_u] = False

            # Postavljanje table u nasumicno stanje, igra moze da se nastavi nakon
            if event.key == pygame.K_n:
                create_random_state(game, config.board_size, config.board_triangle_num, config.board_random_state_max_turns)
                config.show_indexes = True
                print("Tabla je postavljena u nasumično stanje.")
            
            # Resetovanje igre pritiskom na slovo r/R, ne radi kad je igra gotova, vec samo u toku igre
            if event.key == pygame.K_r:
                game.reset()
                config.show_indexes = True
                print("Igra je resetovana.")
            
            # ================================================================================================================
            # Napravljeno samo za testiranje i proveru formiranja mogućih stanja;
            if event.key == pygame.K_f:
                app = form_all_possible_paths(game.pins, config.board_size)
                config.all_possible_states = apply_all_possible_paths(game, app, config.board_size)
                print(f"Formirano {len(config.all_possible_states)} mogućih stanja kao naredni potez.")
                config.show_possible_states = False
            
            elif event.key == pygame.K_p and config.all_possible_states:
                config.show_possible_states = not config.show_possible_states
                print(f"Trenutno je uključeno {'prikazivanje' if config.show_possible_states else 'skrivanje'} mogućih stanja.")
                config.possible_state_ind = 0
            
            elif config.show_possible_states and config.all_possible_states:
                if event.key == pygame.K_RIGHT:
                    config.possible_state_ind = (config.possible_state_ind + 1) % len(config.all_possible_states)
                    print(f"Trenutno je prikazano stanje {config.possible_state_ind+1}/{len(config.all_possible_states)}")
                elif event.key == pygame.K_LEFT:
                    config.possible_state_ind = (config.possible_state_ind - 1) % len(config.all_possible_states)
                    print(f"Trenutno je prikazano stanje {config.possible_state_ind+1}/{len(config.all_possible_states)}")
            # ================================================================================================================

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:  # Levi klik miša
                mouse_pos = event.pos

                clicked_pin: Pin = game.pins.get( get_clicked_pin_area( mouse_pos, config.board_size, config.board_rows_num, config.PLAYABLE_AREA_DIMS,
                                                                        config.ui_top_height, config.board_pin_to_pin_horizontal_distance, config.PADDING,
                                                                        config.board_pin_to_next_row_vertical_distance, config.PADDING ) )

                if clicked_pin and clicked_pin.is_clicked(mouse_pos):
                    if game.selected_pin is None:
                        game.selected_pin = clicked_pin
                        possible_paths = form_all_possible_paths_from_pin(game.selected_pin, game.pins, config.board_size)
                        game.possible_paths = {end_pin: path for end_pin, (_, path) in possible_paths.items()}

                    else: # Ako je već jedan stubić selektovan, pokušaj da se postavi gumica pritiskom na neki drugi stubic

                        if clicked_pin in game.possible_paths:
                            path = game.possible_paths[clicked_pin]
                            # Dodaje novu gumicu
                            game.placed_rubbers.append(Rubber(path[0], path[-1]))

                            connect_pins_and_check_for_triangles(game, path)

                            # Igrač se menja nakon svakog poteza
                            game.swap_current_player()

                            check_for_game_end(game, config.board_triangle_num)
                        else:
                            print("Nemoguće postaviti gumicu do željenog krajnjeg stubića jer nije dovoljno udaljen od početnog ili je već zauzet!")

                        # Resetuje selektovani stubić
                        game.deselect_pin()
            