import pygame


class Theme:
    def __init__(self, _id: str) -> None:
        self._id = _id
        self.themes = {
            "edgy black": {
                "bg_color": (0, 0, 0),
                "font_color": (255, 255, 255),
                "error_color": (255, 0, 0),
                "settings_icon_color": (255, 255, 255),
                "settings_transition_color": (255, 255, 255),
            },
            "captain america": {
                "bg_color": (150, 0, 0),
                "font_color": (0, 255, 255),
                "error_color": (0, 0, 0),
                "settings_icon_color": (255, 255, 255),
                "settings_transition_color": (0, 0, 0),
            },
            "lavender": {
                "bg_color": (35, 0, 64),
                "font_color": (255, 255, 255),
                "error_color": (255, 0, 0),
                "settings_icon_color": (0, 0, 0),
                "settings_transition_color": (0, 0, 0),
            },
            "monkeytype": {
                "bg_color": (50, 52, 55),
                "font_color": (255, 255, 255),
                "error_color": (202, 71, 84),
                "settings_icon_color": (226, 183, 20),
                "settings_transition_color": (226, 183, 20),
            },
            "aqua": {
                "bg_color": pygame.Color("0x22577A"),
                "font_color": (255, 255, 255),
                "error_color": pygame.Color("0x57CC99"),
                "settings_icon_color": (0, 0, 0),
                "settings_transition_color": pygame.Color("0x80ED99"),
            },
            "neo city": {
                "bg_color": pygame.Color("0x1E3163"),
                "font_color": pygame.Color("0x2D46B9"),
                "error_color": pygame.Color("0xF037A5"),
                "settings_icon_color": (0, 0, 0),
                "settings_transition_color": pygame.Color("0xF8F8F8"),
            },
            "unicorn": {
                "bg_color": pygame.Color("0x7C83FD"),
                "font_color": (255, 255, 255),
                "error_color": pygame.Color("0x7DEDFF"),
                "settings_icon_color": pygame.Color("0x96BAFF"),
                "settings_transition_color": pygame.Color("0x88FFF7"),
            },
            "subtle white": {
                "bg_color": pygame.Color("0xF5F5F5"),
                "font_color": (0, 0, 0),
                "error_color": pygame.Color("0xDEECFF"),
                "settings_icon_color": (0, 0, 0),
                "settings_transition_color": pygame.Color("0xDEECFF"),
            }
        }

        (
            self.bg_color,
            self.font_color,
            self.error_color,
            self.settings_icon_color,
            self.settings_transition_color,
        ) = self.themes[_id].values()

    def set_theme(self, settings, console, current_color) -> None:
        # Set console font colors
        console.font_color = self.font_color
        console.font_error_color = self.error_color

        # Set settings icon color
        if current_color != self.settings_icon_color:
            arr = pygame.PixelArray(settings.img)
            arr.replace(current_color, self.settings_icon_color)

        settings.transition_color = self.settings_transition_color
