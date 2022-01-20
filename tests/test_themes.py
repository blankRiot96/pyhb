import unittest
import pygame


class TestThemes(unittest.TestCase):
    def test_themes(self):
        """
        Try loading `Theme` object, test attributes

        :return: None
        """
        from pyhb.typing_tester.themes import Theme
        theme = Theme("lavender")

        self.assertEqual(len(theme.themes), 8)

        try:
            for name in theme.themes:
                for color in theme.themes[name].values():
                    pygame.Color(color)
        except ValueError:
            self.fail("Invalid color argument")


if __name__ == '__main__':
    unittest.main()
