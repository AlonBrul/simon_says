import pygame

"""modes"""
EXIT = -1
PLAY_MOD = 1
MAIN_MOD = 2

"""pygame constants"""
SHOW_SIMON_TURN = pygame.USEREVENT + 1
SIMON_TURN_EVENT = pygame.event.Event(SHOW_SIMON_TURN, show_turn="False")
YOUR_TURN = pygame.USEREVENT + 2
YOUR_TURN_EVENT = pygame.event.Event(YOUR_TURN)

"""sound paths"""
BEEP1 = "./sounds/beep1.ogg"
BEEP2 = "./sounds/beep2.ogg"
BEEP3 = "./sounds/beep3.ogg"
BEEP4 = "./sounds/beep4.ogg"

"""general sizes"""
DISPLAY_DIM = (900, 500)
BUTTON_TEXT_PAD = (45, 10)
BASE_FONT = 15
SMALL_FONT = 35

"""main menu display sizes"""
PLAY_BUTTON_DIM = (50, 150)
INPUT_BOX_DIM = (50, 150)
TOP_PLAYERS_MARGIN = 40

"""game display sizes"""
SQUARE_DIM = (100, 100)
START_BUTTON_DIM = (50, 150)
RESTART_BUTTON_DIM = (50, 200)
BACK_BUTTON_DIM = (50, 200)
REDO_BUTTON_DIM = (50, 200)

"""main menu display positions"""
PLAY_BUTTON_POS = (400, 200)
MAIN_TEXT_MENU_POS = (350, 50)
ENTER_NAME_TEXT_POS = (400, 90)
INPUT_BOX_POS = (400, 120)
CURRENT_PLAYER_POS = (405, 125)
TOP_PLAYERS_TEXT_POS = (50, 50)
TOP_PLAYERS_POS = (50, 80)

"""game positions (TL = top left,...)"""
TL_BUTTON_POS = (350, 150)
TR_BUTTON_POS = (500, 150)
BL_BUTTON_POS = (350, 260)
BR_BUTTON_POS = (500, 260)
START_BUTTON_POS = (400, 50)
RESTART_BUTTON_POS = (10, 80)
BACK_BUTTON_POS = (10, 150)
REDO_TEXT_POS = (360, 370)
REDO_BUTTON_POS = (360, 400)
SCORE_TEXT_POS = (10, 10)
MAIN_TEXT_GAME_POS = (400, 50)

"""colors"""
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BRIGHT_RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BRIGHT_BLUE = (0, 0, 255)
GREEN = (50, 205, 50)
BRIGHT_GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PASSIVE_INPUT = pygame.Color('gray')
ACTIVE_INPUT = pygame.Color('lightskyblue3')
