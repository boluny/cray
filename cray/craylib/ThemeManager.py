import os

class ThemeManager(object):
    """manager of themes"""

    def __init__(self, theme_dir):
        self.__theme_dir = theme_dir
        self.__theme = []

    def set_theme(self, theme_name):
        self.__theme_name = theme_name
        self.__tpl_index = os.path.join(self.__theme_dir, self.__theme_name, "index.html")
        self.__tpl_post = os.path.join(self.__theme_dir, self.__theme_name, "post.html")
        self.__tpl_page = os.path.join(self.__theme_dir, self.__theme_name, "page.html")

    def is_theme_usable(self):
        if os.path.exists(self.__tpl_index) \
            and os.path.exists(self.__tpl_page) \
            and os.path.exists(self.__tpl_post):
            return True

        return False
        
    def get_current_theme(self):
        pass

    def get_template_path(self):
        if not self.is_theme_usable():
            return None

        return dict(index = self.__tpl_index, post = self.__tpl_post, page = self.__tpl_page)

    def get_abs_path(self):
        return os.path.join(self.__theme_dir, self.__theme_name)

