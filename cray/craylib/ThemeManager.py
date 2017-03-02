class ThemeManager(object):
    """manager of themes"""

    def __init__(self, theme_dir):
        self._theme_dir = theme_dir
        self._theme = []

    def set_theme(self, theme_name):
        self._theme_name = theme_name

    def is_theme_usable(self):
        pass

    def get_current_theme():
        pass

