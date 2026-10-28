# pokretanje: python .\main.py
import pygame

import sys

import config
from models import *
from game_logic import *
from drawing import *

def main():

    game = Game()

    game.game_mode = draw_choose_gamemode_window()
    print(f"Izabran mod igre: {game.game_mode}")

    game.current_player = draw_choose_first_player_window(game.game_mode)
    print(f"Izabrani prvi igrač: {game.current_player}")    

    config.board_size = draw_choose_board_size_window()
    print(f"Izabrana veličina stranice table: {config.board_size}")
    config.board_rows_num = config.board_size * 2 - 1
    config.board_triangle_num = calculate_total_triangles_num(config.board_size)
    config.board_pin_to_pin_horizontal_distance = config.PLAYABLE_AREA_WIDTH / (config.board_rows_num- 1)

    pygame.init()
    pygame.display.set_caption(config.CAPTION)
    config.SCREEN = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    config.ui_top_height = draw_ui(config.SCREEN, game.x_token_num, game.o_token_num, game.random_state, game.current_player, game.game_over)
    config.board_pin_to_next_row_vertical_distance = (config.PLAYABLE_AREA_HEIGHT - config.ui_top_height) / (config.board_rows_num - 1)

    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    KONTROLE NA TASTATURI:                     ║
    ╠═══════╦═══════════════════════════════════════════════════════╣
    ║  [T]  ║ Prikaz indeksa iznad stubića                          ║
    ║  [N]  ║ Postavljanje table u nasumično stanje                 ║
    ║  [R]  ║ Resetovanje table u toku igre                         ║
    ╠═══════╬═══════════════════════════════════════════════════════╣
    ║  [F]  ║ Formiranje svih mogućih stanja table                  ║
    ║       ║(gde je 1 novo stanje 1 odigran potez trenutnog igrača)║
    ╠═══════╬═══════════╦═══════════════════════════════════════════╣
    ║       ║    [P]    ║ Prikazivanje mogućih stanja               ║
    ║       ║  [←]/[→]  ║ Prelazak na naredno moguće stanje         ║
    ╚═══════╩═══════════╩═══════════════════════════════════════════╝
""")

    # Main loop, radi beskonačno i ovde se pozivaju sve glavne f-je za igranje
    running = True
    while running:

        if game.pins:
            if game.game_mode == 'Protiv kompjutera' and game.current_player ==  "O" and not game.game_over:
                computers_turn(game)
            
            humans_turn(game, sys)

        # ISCRTAVANJE SVEGA:

        # Crna pozadina
        config.SCREEN.fill((21, 21, 21))

        # Kreiranje table
        if not game.pins:
            config.ui_top_height = draw_ui(config.SCREEN, game.x_token_num, game.o_token_num, game.random_state, game.current_player, game.game_over)
            game.pins = create_board(config.board_size, config.PLAYABLE_AREA_DIMS, config.ui_top_height, config.PADDING)

        # iscrtava oblasti oko pinova koje oni zauzimaju
        # draw_pin_areas(config.SCREEN, config.board_size, config.board_rows_num, config.PLAYABLE_AREA_WIDTH,
        #                config.board_pin_to_pin_horizontal_distance, config.PADDING, config.board_pin_to_next_row_vertical_distance, config.PADDING)


        if config.show_possible_states and config.all_possible_states:
            config.ui_top_height = draw_ui(config.SCREEN, config.all_possible_states[config.possible_state_ind].x_token_num, config.all_possible_states[config.possible_state_ind].o_token_num,
                                           game.random_state, config.all_possible_states[config.possible_state_ind].current_player, config.all_possible_states[config.possible_state_ind].game_over)
            draw_rubbers(config.SCREEN, config.all_possible_states[config.possible_state_ind].placed_rubbers)
            draw_tokens(config.SCREEN, config.all_possible_states[config.possible_state_ind].placed_tokens)
        else:
            config.ui_top_height = draw_ui(config.SCREEN, game.x_token_num, game.o_token_num, game.random_state, game.current_player, game.game_over)
            draw_rubbers(config.SCREEN, game.placed_rubbers)
            draw_tokens(config.SCREEN, game.placed_tokens)



        draw_pins(config.SCREEN, game.pins, config.show_indexes)

        # Iscrtavanje validnih puteva za selektovani stubić
        draw_all_possible_paths(config.SCREEN, game.possible_paths)

        if game.game_over: # ako je igra gotova, ispisuje se ko je pobednik na sredini prozora
            draw_game_over_text(config.SCREEN, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, game.winner, game.winning_token_num)

        # Ažuriranje prikaza
        pygame.display.flip()


# ==========================================================================================================================================
# ==========================================================================================================================================
# ==========================================================================================================================================

if __name__ == "__main__":
    main()

# ==========================================================================================================================================
# ==========================================================================================================================================
# ==========================================================================================================================================
