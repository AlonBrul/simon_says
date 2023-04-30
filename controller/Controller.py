import time
import sys
from model import model
from constants import *
from threading import Timer
from db import *


class Controller:
    """ This class represent the main controller, the main controller is responsible to switch between different
     controllers.
      :param view: the main view class.
      :param rows: a list of tuples that represent the score table.
      :param conn: a connection to the database.
      :return:
      """
    def __init__(self, view, rows, conn):
        self.current_player = model.Text("", CURRENT_PLAYER_POS)
        self.players_and_scores = rows
        self.game_controller = GameController(view, self.current_player, self.players_and_scores, conn)
        self.main_controller = MainMenuController(view, self.current_player, self.players_and_scores, conn)
        self.mode = MAIN_MOD
        self.view = view
        self.db_conn = conn

    def run(self):
        """ This function is responsible to get the events and pass them to the controllers.
        Each iteration of the while loop in this function is a frame.
          :param
          :return:
          """
        clock = pygame.time.Clock()
        while self.mode is not EXIT:
            clock.tick(60)

            events = pygame.event.get()
            if self.mode == PLAY_MOD:
                mode_tmp = self.game_controller.run(events)
            else:
                mode_tmp = self.main_controller.run(events)
            if mode_tmp != self.mode:
                if mode_tmp == MAIN_MOD:
                    self.players_and_scores = self.game_controller.players_and_scores

                self.mode = mode_tmp
                self.game_controller = GameController(self.view, self.current_player, self.players_and_scores,
                                                      self.db_conn)
                self.main_controller = MainMenuController(self.view, self.current_player, self.players_and_scores,
                                                          self.db_conn)

                self.view.reset_view()

        pygame.quit()
        sys.exit()


class AbstractController:
    """ This is an abstract class. The MainController and GameController inherit this
    class. A controller is responsible to show objects, handle events and dictate game flow
      :param
      :return:
      """

    def __init__(self, view, current_player, players_and_scores, conn):
        self.view = view
        self.current_player = current_player
        self.players_and_scores = players_and_scores
        self.to_display = []
        self.main_text = None
        self.sleep = False
        self.keepGoing = True
        self.db_conn = conn

    def init_window(self):
        """ Show all object that are in to_display list
          :param
          :return:
          """
        self.view.show_window(self.to_display)

    def update_main_txt(self, txt):
        """ Update the main_text object
          :param txt: the new text we want to show on the screen
          :return:
          """
        self.view.reset_view()
        self.main_text.msg = txt
        if self.main_text not in self.to_display:
            self.to_display.append(self.main_text)
        self.sleep = True


class GameController(AbstractController):
    """ The controller that handle all events in the play screen.
      :param
      :return:
      """
    def __init__(self, view, current_player, players_and_scores, conn):
        super().__init__(view, current_player, players_and_scores, conn)
        self.simon = model.Simon()
        self.player = model.Player(current_player.msg, players_and_scores)
        self.keepGoing = PLAY_MOD
        self.squares = [
            model.Button(SQUARE_DIM, TL_BUTTON_POS, GREEN, BEEP1, on_click=self.handle_square_event(0)),
            model.Button(SQUARE_DIM, TR_BUTTON_POS, RED, BEEP2, on_click=self.handle_square_event(1)),
            model.Button(SQUARE_DIM, BL_BUTTON_POS, YELLOW, BEEP3, on_click=self.handle_square_event(2)),
            model.Button(SQUARE_DIM, BR_BUTTON_POS, BLUE, BEEP4, on_click=self.handle_square_event(3))]
        self.start_button = model.Button(START_BUTTON_DIM, START_BUTTON_POS, ORANGE, on_click=self.handle_start_event(),
                                         text="Start")
        self.restart_button = model.Button(RESTART_BUTTON_DIM, RESTART_BUTTON_POS, GREEN, on_click=self.restart,
                                           text="Try again")
        self.back_button = model.Button(BACK_BUTTON_DIM, BACK_BUTTON_POS, ORANGE, on_click=self.handle_back_event,
                                        text="Main menu")
        self.redo_txt = model.Text("Click the button bellow to return to the previous stage", REDO_TEXT_POS, True)
        self.redo_button = model.Button(REDO_BUTTON_DIM, REDO_BUTTON_POS, ORANGE, on_click=self.handle_prev_lvl,
                                        text="Previous level")
        self.score_txt = model.Text("Score : 0", SCORE_TEXT_POS)
        self.simon_turn = False
        self.main_text = model.Text("Simon's Turn", MAIN_TEXT_GAME_POS)
        self.originator = model.Originator()
        self.states = []
        self.to_display = [*self.squares, self.start_button, self.score_txt]
        self.clickable = [*self.squares, self.start_button]
        self.blinks = 0
        self.sleep_time = 1
        self.sleep = False
        self.game_started = False

    def restart(self):
        """ Reset the GameController object to initial values
          :param
          :return:
          """
        self.view.reset_view()
        self.__init__(self.view, self.current_player, self.players_and_scores, self.db_conn)

    def run(self, events):
        """ Runs the game, each call of this function is a frame
          :param events: a list of pygame events
          :return: the next mod we want to be
          """
        for event in events:
            if event.type == pygame.QUIT:
                self.keepGoing = EXIT
            elif event.type == SHOW_SIMON_TURN:
                if event.show_turn == "True":
                    self.show_simon_turn()
                else:
                    self.sleep = True
                    self.show_steps()
            elif event.type == YOUR_TURN:
                self.sleep = False
                self.show_player_turn()

        event_pos = get_mouseclick_pos(events)
        self.handle_events(event_pos)
        self.check_turn()
        self.init_window()
        if self.sleep:
            time.sleep(self.sleep_time)
            self.sleep = False

        return self.keepGoing

    def handle_events(self, pos):
        """ Handle user mouse click events
          :param pos: if user clicked on the screen, pos represent the click position
          :return:
          """
        if pos:
            for button in self.clickable:
                rect = self.view.get_pygame_rect_from_rect(button)
                if rect.collidepoint(pos):
                    if not self.simon_turn:
                        button.on_click()
                    elif button == self.restart_button:
                        button.on_click()
                    elif button == self.back_button:
                        button.on_click()
                    elif button == self.redo_button:
                        button.on_click()
                    return

    def handle_square_event(self, i):
        """
          :param i: index of a button in our squares list
          :return: a function to be called when a user clicked on a square
          """
        return lambda: self.handle_player_move(i)

    def handle_start_event(self):
        """ This function block user click event.
          :param
          :return a function to be called when a user clicks on start button:
          """
        return self.show_simon_turn

    def handle_back_event(self):
        """ This function sets the next mod to be the main mod. in the next frame screen will return to main menu
          :param
          :return:
          """
        self.keepGoing = MAIN_MOD

    def handle_player_move(self, index):
        """ This function check if user clicked the right square, also this function is responsible to
        make the squares blink and to let the user know if he was wrong.
          :param index: index of a square in our squares list
          :return:
          """
        if self.game_started:
            if self.simon.challenge[len(self.player.steps_done)] == index:
                self.blink(index, False)
                self.player.steps_done.append(index)
            else:
                self.show_fail_screen()
                self.simon_turn = True
                insert_row(self.db_conn, (self.player.name, self.player.total_score))
                self.players_and_scores = get_all_rows(self.db_conn)

    def show_fail_screen(self):
        super().update_main_txt("Oh no! Wrong answer :( ")
        self.add_button(self.restart_button)
        self.add_button(self.back_button)
        if self.simon.lvl > 1:
            self.add_button(self.redo_button)
            self.to_display.append(self.redo_txt)

    def show_simon_turn(self, custom_lvl=None):
        """
          :param
          :return:
          """
        self.simon_turn = True
        self.game_started = True
        self.view.reset_view()
        self.simon.init_challenge(custom_lvl)
        self.originator.set(self.simon.challenge[:])
        self.states.append(self.originator.save_to_memento())
        if self.start_button in self.to_display:
            self.remove_button(self.start_button)
        super().update_main_txt("Simon's Turn")
        pygame.event.post(SIMON_TURN_EVENT)

    def handle_prev_lvl(self):
        self.remove_button(self.restart_button)
        self.remove_button(self.back_button)
        self.remove_button(self.redo_button)
        self.to_display.remove(self.redo_txt)
        self.originator.restore_from_memento(self.states[-2])
        prev_lvl = self.originator.save_to_memento().get_saved_state()
        self.states.pop()
        self.show_simon_turn(custom_lvl=prev_lvl)

    def show_player_turn(self):
        """Letting the user know that now is the user turn
          :param
          :return:
          """
        self.view.reset_view()
        super().update_main_txt("Your Turn")

    def show_steps(self):
        """ Showing the user the steps he needs to follow
          :param
          :return:
          """
        if len(self.simon.steps_to_show) > 0:
            index = self.simon.steps_to_show.pop(0)
            self.blink(index, True)
        if len(self.simon.steps_to_show) > 0:
            pygame.event.post(SIMON_TURN_EVENT)

    def blink(self, index, update_blinks):
        """ Making a square blink and also make a sound
          :param index: represent a index in the squares list.
          :param update_blinks: if we want to count this as a simon step or user step
          :return:
          """
        square = self.squares[index]
        square.set_color(square.secondary_color)
        pygame.mixer.music.load(square.sound_path)
        pygame.mixer.music.play(0)

        def change_color_back():
            square.set_color(square.main_color)
            if update_blinks:
                self.blinks += 1

        timer = Timer(0.3, change_color_back)
        timer.start()

    def check_turn(self):
        """ Checks if its the user's turn or simon's turn
          :param
          :return:
          """
        if self.blinks == self.simon.lvl:
            self.blinks = 0
            self.simon_turn = False
            pygame.event.post(YOUR_TURN_EVENT)
        elif len(self.player.steps_done) == self.simon.lvl:
            self.player.steps_done = []
            super().update_main_txt("Good Job!")
            self.simon.lvl += 1
            self.player.score += 10
            self.player.total_score += 10
            self.score_txt.msg = f"Score: {self.player.score}"
            event = pygame.event.Event(SHOW_SIMON_TURN, show_turn="True")
            timer = Timer(1, lambda: pygame.event.post(event))
            timer.start()

    def add_button(self, button):
        self.to_display.append(button)
        self.clickable.append(button)

    def remove_button(self, button):
        self.to_display.remove(button)
        self.clickable.remove(button)


class MainMenuController(AbstractController):
    """ This is the controller that responsible to handle the events in the main menu and decides what to show on the
    screen
      :param
      :return:
      """

    def __init__(self, view, current_player, players_and_scores, conn):
        super().__init__(view, current_player, players_and_scores, conn)
        self.main_text = model.Text("Welcome to Simon!", MAIN_TEXT_MENU_POS)
        self.enter_your_name = model.Text("Please enter your name bellow:", ENTER_NAME_TEXT_POS, small=True)
        self.play_button = model.Button(PLAY_BUTTON_DIM, PLAY_BUTTON_POS, ORANGE, on_click=self.change_mod,
                                        text="Play")
        self.input_box = model.Button(INPUT_BOX_DIM, INPUT_BOX_POS, PASSIVE_INPUT, on_click=self.handle_input_active)
        self.top_players = model.Text("Top 5 players:", TOP_PLAYERS_TEXT_POS)
        self.input_active = False
        self.to_display = [self.main_text, self.play_button, self.input_box, self.enter_your_name, self.top_players]
        self.clickable = [self.play_button, self.input_box]
        self.keepGoing = MAIN_MOD
        self.show_top_players()

    def run(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.keepGoing = EXIT
            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.current_player.msg = self.current_player.msg[:-1]
                    self.input_box.set_text_msg(self.current_player.msg.strip())
                else:
                    self.current_player.msg += event.unicode
                    self.input_box.set_text_msg(self.current_player.msg.strip())
                self.view.reset_view()

        event_pos = get_mouseclick_pos(events)
        self.handle_events(event_pos)
        if self.input_active:
            self.input_box.set_color(ACTIVE_INPUT)
        else:
            self.input_box.set_color(PASSIVE_INPUT)

        self.init_window()
        return self.keepGoing

    def change_mod(self):
        tmp_name = self.current_player.msg.replace(" ", "")
        if tmp_name != "":
            self.keepGoing = PLAY_MOD

    def handle_events(self, pos):
        if pos:
            for rectangle in self.clickable:
                rect = self.view.get_pygame_rect_from_rect(rectangle)
                if rect.collidepoint(pos):
                    rectangle.on_click()
                else:
                    self.input_active = False

    def handle_input_active(self):
        self.input_active = True

    def show_top_players(self):
        """ This function displays the top players table
          :param
          :return:
          """
        index = 0
        for name, score in self.players_and_scores:
            tmp_txt = model.Text(f"{index}) {name} : {score}", (TOP_PLAYERS_POS[0], TOP_PLAYERS_POS[1] +
                                                                index * TOP_PLAYERS_MARGIN))
            self.to_display.append(tmp_txt)
            index += 1


def get_mouseclick_pos(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            return pygame.mouse.get_pos()
