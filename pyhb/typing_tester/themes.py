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
            },
            "captain america": {
                "bg_color": (150, 0, 0),
                "font_color": (0, 255, 255),
                "error_color": (0, 0, 0),
                "settings_icon_color": (255, 255, 255),
            },
            "lavender": {
                "bg_color": (35, 0, 64),
                "font_color": (255, 255, 255),
                "error_color": (255, 0, 0),
                "settings_icon_color": (0, 0, 0),
            },
        }

        (
            self.bg_color,
            self.font_color,
            self.error_color,
            self.settings_icon_color,
        ) = self.themes[_id].values()

        if _id == "edgy black":
            self.settings_transition_color = (255, 255, 255)
        else:
            self.settings_transition_color = (1, 0, 0)

    def set_theme(self, settings, console) -> None:
        # Set console font colors
        console.font_color = self.font_color
        console.font_error_color = self.error_color

        # Set settings icon color
        if self.settings_icon_color != (0, 0, 0):
            arr = pygame.PixelArray(settings.img)
            arr.replace((0, 0, 0), self.settings_icon_color)
        settings.transition_color = self.settings_transition_color
