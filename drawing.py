import pygame

import sys

from models import *

def draw_choose_gamemode_window():
    pygame.init()
    game_mode = None

    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Trouglići")

    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    orange = (255, 165, 0)
    hover_color = (135, 206, 250)

    font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)

    question_text = font.render("Izaberi mod igre", True, white)
    question_rect = question_text.get_rect(center=(width / 2, height / 4))

    pvc_text = button_font.render("Protiv kompjutera", True, black)
    pvp_text = button_font.render("Protiv drugog igraca", True, black)

    button_width, button_height = 250, 80
    pvc_rect = pygame.Rect((width / 4 - button_width / 2, height / 2 - button_height / 2),
                           (button_width, button_height))
    pvp_rect = pygame.Rect((3 * width / 4 - button_width / 2, height / 2 - button_height / 2),
                           (button_width, button_height))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pvc_rect.collidepoint(event.pos):
                    running = False
                    game_mode = "Protiv kompjutera"
                elif pvp_rect.collidepoint(event.pos):
                    running = False
                    game_mode = "Protiv drugog igraca"

        # Hover efekti
        pvc_color = hover_color if pvc_rect.collidepoint(mouse_pos) else green
        pvp_color = hover_color if pvp_rect.collidepoint(mouse_pos) else orange

        screen.fill(black)
        screen.blit(question_text, question_rect)

        # Iscrtavanje dugmadi sa hover efektima
        pygame.draw.rect(screen, pvc_color, pvc_rect)
        pygame.draw.rect(screen, white, pvc_rect, 2)
        screen.blit(pvc_text, pvc_text.get_rect(center=pvc_rect.center))

        pygame.draw.rect(screen, pvp_color, pvp_rect)
        pygame.draw.rect(screen, white, pvp_rect, 2)
        screen.blit(pvp_text, pvp_text.get_rect(center=pvp_rect.center))

        pygame.display.flip()

    pygame.quit()
    return game_mode


# -------------------------------------------------------------------

def draw_choose_first_player_window(game_mode):
    pygame.init()
    player = None

    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Trouglići")

    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    orange = (255, 165, 0)
    hover_color = (135, 206, 250)

    font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)

    question_text = font.render("Ko igra prvi?", True, white)
    question_rect = question_text.get_rect(center=(width / 2, height / 4))

    player1_text = button_font.render("Igrač X", True, black)
    if game_mode == "Protiv kompjutera":
        player2_text = button_font.render("Kompjuter O", True, black)
    else:
        player2_text = button_font.render("Igrač O", True, black)

    button_width, button_height = 250, 80
    player1_rect = pygame.Rect((width / 4 - button_width / 2, height / 2 - button_height / 2),
                               (button_width, button_height))
    player2_rect = pygame.Rect((3 * width / 4 - button_width / 2, height / 2 - button_height / 2),
                               (button_width, button_height))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player1_rect.collidepoint(event.pos):
                    running = False
                    player = Game.PLAYER_X
                elif player2_rect.collidepoint(event.pos):
                    running = False
                    player = Game.PLAYER_O

        # Hover efekti
        player1_color = hover_color if player1_rect.collidepoint(mouse_pos) else green
        player2_color = hover_color if player2_rect.collidepoint(mouse_pos) else orange

        screen.fill(black)
        screen.blit(question_text, question_rect)

        # X dugme
        pygame.draw.rect(screen, player1_color, player1_rect)
        pygame.draw.rect(screen, white, player1_rect, 2)
        screen.blit(player1_text, player1_text.get_rect(center=player1_rect.center))

        # O dugme
        pygame.draw.rect(screen, player2_color, player2_rect)
        pygame.draw.rect(screen, white, player2_rect, 2)
        screen.blit(player2_text, player2_text.get_rect(center=player2_rect.center))

        pygame.display.flip()

    pygame.quit()
    return player


# -------------------------------------------------------------------

def draw_choose_board_size_window():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Unos veličine table')

    white = (255, 255, 255)
    black = (0, 0, 0)
    hover_yellow = (255, 255, 50)
    blue = (100, 149, 237)
    hover_blue = (65, 105, 225)

    font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)

    # Moguce velicine table
    min_value = 4
    max_value = 8
    value = 4

    box_rect = pygame.Rect(width // 2 - 100, height // 2 - 60, 200, 80)
    up_button_rect = pygame.Rect(box_rect.right + 20, box_rect.top, 80, 40)
    down_button_rect = pygame.Rect(box_rect.right + 20, box_rect.bottom - 40, 80, 40)
    ok_button_rect = pygame.Rect(width // 2 - 60, box_rect.bottom + 40, 120, 50)

    title_text = font.render("Izaberite veličinu table:", True, white)
    title_rect = title_text.get_rect(center=(width // 2, height // 3))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if up_button_rect.collidepoint(mouse_pos):
                    if value < max_value:
                        value += 1
                elif down_button_rect.collidepoint(mouse_pos):
                    if value > min_value:
                        value -= 1
                elif ok_button_rect.collidepoint(mouse_pos):
                    running = False

        up_button_color = hover_yellow if up_button_rect.collidepoint(mouse_pos) else white
        down_button_color = hover_yellow if down_button_rect.collidepoint(mouse_pos) else white
        ok_button_color = hover_blue if ok_button_rect.collidepoint(mouse_pos) else blue

        screen.fill(black)
        screen.blit(title_text, title_rect)

        # Trenutna vrednost
        value_text = font.render(str(value), True, black)
        value_rect = value_text.get_rect(center=box_rect.center)
        pygame.draw.rect(screen, white, box_rect)
        screen.blit(value_text, value_rect)

        # Gore
        pygame.draw.rect(screen, up_button_color, up_button_rect)
        up_text = button_font.render("+", True, black)
        up_text_rect = up_text.get_rect(center=up_button_rect.center)
        screen.blit(up_text, up_text_rect)

        # Dole
        pygame.draw.rect(screen, down_button_color, down_button_rect)
        down_text = button_font.render("-", True, black)
        down_text_rect = down_text.get_rect(center=down_button_rect.center)
        screen.blit(down_text, down_text_rect)

        # OK
        pygame.draw.rect(screen, ok_button_color, ok_button_rect)
        ok_text = button_font.render("OK", True, white)
        ok_text_rect = ok_text.get_rect(center=ok_button_rect.center)
        screen.blit(ok_text, ok_text_rect)

        pygame.display.flip()

    pygame.quit()
    return value

# -------------------------------------------------------------------

def token_num_grammar_correction(count: int, word: str):
    return f"{word}" if count == 1 else f"{word}a"

def draw_ui(screen, x_token_num, o_token_num, is_random_state, current_player, is_game_over):
    """Ispisuje neke informacije na vrhu (koliko svaki igrac ima trouglića i da li je iskorišćeno nasumično stanje)."""
    font = pygame.font.Font(None, 36)

    text_x = f"{Game.PLAYER_X}: {x_token_num} {token_num_grammar_correction(x_token_num, Game.TOKEN_NUM_TAG)}"
    text_o = f"{Game.PLAYER_O}: {o_token_num} {token_num_grammar_correction(o_token_num, Game.TOKEN_NUM_TAG)}"

    if is_random_state:
        text_random = "NASUMIČNO STANJE"
        random_surface = font.render(text_random, True, (0, 0, 0))
        random_rect = random_surface.get_rect(center=(screen.get_width() / 2, 25))
        pygame.draw.rect(screen, (255, 255, 255), random_rect.inflate(10, 10))
        screen.blit(random_surface, random_rect)

    x_surface = font.render(text_x, True, (0, 0, 0))  # tekst ce biti crne boje
    o_surface = font.render(text_o, True, (0, 0, 0))

    x_rect = x_surface.get_rect(topleft=(10, 10))  # X u gornjem levom uglu
    o_rect = o_surface.get_rect(topright=(screen.get_width() - 10, 10))  # O u gornjem desnom uglu

    pygame.draw.rect(screen, (255, 255, 255), x_rect.inflate(10, 10))  # Pozadina za X
    pygame.draw.rect(screen, (255, 255, 255), o_rect.inflate(10, 10))  # Pozadina za O

    # Iscrtavanje teksta
    screen.blit(x_surface, x_rect)
    screen.blit(o_surface, o_rect)

    if not is_game_over:
        moderate_font = pygame.font.Font(None, 28)
        text_player = f"Trenutno na potezu: {current_player}"
        player_surface = moderate_font.render(text_player, True, (0, 0, 0))
        player_rect = player_surface.get_rect()

        if current_player == Game.PLAYER_X:
            player_rect.bottomleft = (10, screen.get_height() - 10)
        else:
            player_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)

        padding = 8
        background_rect = player_rect.inflate(padding * 2, padding * 2)
        background_surface = pygame.Surface(background_rect.size, pygame.SRCALPHA)
        background_surface.fill((255, 255, 255, 150))  # Semi-transparent white

        text_rect = player_surface.get_rect(center=background_rect.center)

        screen.blit(background_surface, background_rect.topleft)
        screen.blit(player_surface, text_rect)



    return max(x_rect.height, o_rect.height)  # Vraca visinu gornjeg dela kako bi se tabla iscrtala ispod


# -------------------------------------------------------------------

def draw_pins(screen, pins, show_pin_indexes):
    for pin in pins.values():
            pin.draw(screen, show_pin_indexes)

# -------------------------------------------------------------------

def draw_possible_path(screen, possible_path, color):
    """Označava sve stubiće koji predstavljaju jedan mogući put."""
    for pin in possible_path:
        pygame.draw.circle(screen, color, (pin.x, pin.y), 8)

    if possible_path:  # iscrtava okvir oko prvog i poslednjeg stubića puta
        start_pin = possible_path[0]
        pygame.draw.circle(screen, (255, 74, 0), (start_pin.x, start_pin.y), 10, 3)

        end_pin = possible_path[-1]
        pygame.draw.circle(screen, (255, 74, 0), (end_pin.x, end_pin.y), 10, 3)

# -------------------------------------------------------------------

def draw_all_possible_paths(screen, possible_paths):
    for path in possible_paths.values():
            draw_possible_path(screen, path, (255, 255, 0))

# -------------------------------------------------------------------

def draw_rubbers(screen, placed_rubbers):
    for rubber in placed_rubbers:
            rubber.draw(screen)

# -------------------------------------------------------------------

def draw_tokens(screen, placed_tokens):
    for token in placed_tokens:
        token.draw(screen)

# -------------------------------------------------------------------

def draw_game_over_text(screen, screen_width, screen_height, winner, winning_token_num):
    """ Prikazuje tekst za kraj igre na ekranu. """
    font = pygame.font.SysFont("Arial", 40)

    text = font.render("IGRA JE GOTOVA", True, (0, 0, 0))

    if winner == "Nerešeno":
        winner_text = font.render("Nerešeno", True, (0, 0, 0))
    else:
        winner_text = font.render(f"Pobednik je {winner} sa {winning_token_num} trouglića", True, (0, 0, 0))

    # Pozicija teksta na ekranu
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    winner_rect = winner_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    padding = 10

    # Pravougaonici za pozadinu teksta
    pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(padding * 2, padding))
    pygame.draw.rect(screen, (255, 255, 255), winner_rect.inflate(padding * 2, padding))

    screen.blit(text, text_rect)
    screen.blit(winner_text, winner_rect)

# -------------------------------------------------------------------

def draw_pin_areas(screen, board_size, board_rows_num, playable_area_width, pin_area_width, pin_area_height, pin_area_row_margin, padding):
    board_top_left = (padding, padding)

    for current_row in range(board_rows_num):
        if current_row < board_size:
            current_row_length = board_size + current_row  # redovi pre srednjeg reda
        else:
            current_row_length = board_size + (board_rows_num - 1 - current_row)  # redovi posle srednjeg reda
        
        # offset za centriranje svakog reda
        current_row_offset = (playable_area_width - current_row_length * pin_area_width) // 2
        
        for col in range(current_row_length):
            x = board_top_left[0] + col * pin_area_width + current_row_offset
            y = board_top_left[1] + current_row * (pin_area_height + pin_area_row_margin - padding)
            pygame.draw.rect(screen, (200, 200, 200), (x, y, pin_area_width, pin_area_height), 2)
