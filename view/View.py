from model import model
from constants import *

FPS = 60


class View:
    """ View class is responsible to show the object on the screen
    :param
    :return:
    """
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode(DISPLAY_DIM)
        self.win.fill(BLACK)
        self.base_font = pygame.font.SysFont('Corbel', BASE_FONT)
        self.small_font = pygame.font.SysFont('Corbel', SMALL_FONT)
        pygame.display.set_caption("Simon Says")

    def reset_view(self):
        """ Reset the screen, paint it all the to base color
        :param
        :return:
        """
        self.win.fill(BLACK)

    def show_window(self, objects):
        """ Show list of objects on the screen
        :param objects : a list of object that we can show on the screen. Can be only Text or Rectangle instances.
        :return:
        """
        for object_to_show in objects:
            if isinstance(object_to_show, model.Rectangle):
                self.show_rectangle(object_to_show)
            elif isinstance(object_to_show, model.Text):
                self.show_text(object_to_show)

    def show_rectangle(self, rect):
        """ shows Rectangle object on the screen
        :param rect: can be Rectangle only
        :return:
        """
        if isinstance(rect, model.Button):
            pygame_rect = self.get_pygame_rect_from_rect(rect)
            if rect.has_text_msg():
                text = self.small_font.render(rect.get_text_msg(), True, WHITE)
                pygame_rect.width = max(rect.get_width(), text.get_width() + BUTTON_TEXT_PAD[0])
                pygame.draw.rect(self.win, rect.color, pygame_rect)
                self.show_text(rect.text)
            else:
                pygame.draw.rect(self.win, rect.color, pygame_rect)
        else:
            pygame_rect = self.get_pygame_rect_from_rect(rect)
            pygame.draw.rect(self.win, rect.color, pygame_rect)
        pygame.display.update()

    def show_text(self, txt):
        """ Shows Text object on the screen
        :param txt: An Text typed object.
        :return:
        """
        if txt.small is True:
            text = self.base_font.render(txt.msg, True, WHITE)
        else:
            text = self.small_font.render(txt.msg, True, WHITE, )
        self.win.blit(text, txt.pos)
        pygame.display.update()

    def get_pygame_rect_from_rect(self, rect):
        """ This function gets a Rectangle object and returns Pygame.Rect
        :param rect: Rectangle object
        :return: pygame.Rect
        """
        return pygame.Rect(rect.position[0], rect.position[1], rect.get_width(), rect.get_height())
