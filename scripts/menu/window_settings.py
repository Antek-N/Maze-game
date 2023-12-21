import pygame
import pygame_menu


class WindowSettings:
    """
    A class setting and containing window settings for a game.

    :cvar int DISPLAY_WIDTH: The width of the display.
    :cvar int DISPLAY_HEIGHT: The height of the display.
    :cvar DISPLAY: The display object.
    :cvar THEME: The pygame_menu theme object.
    """
    DISPLAY_WIDTH = 0
    DISPLAY_HEIGHT = 0
    DISPLAY = None
    THEME = None

    def initialize_settings(self) -> None:
        """
        Initializes the window settings by setting the program title, icon, display size, display, and theme.
        (main method of the class)

        :param: None
        :return: None
        """
        self.set_program_title()
        self.set_program_icon()
        self.set_display_size()
        self.set_display()
        self.set_theme()

    @staticmethod
    def set_program_title() -> None:
        """
        Sets the program title.

        :param: None
        :return: None
        """
        pygame.display.set_caption("DotGame")

    @staticmethod
    def set_program_icon() -> None:
        """
        Sets the program icon.

        :param: None
        :return: None
        """
        pygame.display.set_icon(pygame.image.load(r'img/icon.png'))

    @staticmethod
    def set_theme() -> None:
        """
        Sets the pygame_menu theme.

        :param: None
        :return: None
        """
        bg_image = pygame_menu.baseimage.BaseImage(
            image_path=r"img/theme.jpg",
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
            drawing_offset=(0, 0))

        WindowSettings.THEME = pygame_menu.Theme(
            background_color=bg_image,
            title_background_color=(0, 0, 0),
            title_font_color=(40, 40, 40),
            title_font_shadow=False,
            widget_padding=25,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            cursor_color=(200, 0, 0),
            selection_color=(140, 0, 0),
            widget_font_color=(40, 40, 40))

    @staticmethod
    def set_display_size() -> None:
        """
        Sets the display size based on the current resolution.

        :param: None
        :return: None
        """
        display_resolution = pygame.display.Info()
        WindowSettings.DISPLAY_WIDTH, WindowSettings.DISPLAY_HEIGHT = display_resolution.current_w, display_resolution.current_h

    @staticmethod
    def set_display():
        """
        Sets the display.

        :param: None
        :return: None
        """
        WindowSettings.DISPLAY = pygame.display.set_mode((WindowSettings.DISPLAY_WIDTH, WindowSettings.DISPLAY_HEIGHT))
