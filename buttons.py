__author__ = 'MazeFX'
#!/usr/bin/kivy

# TODO - Clean up file

import os.path
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.actionbar import ActionButton
from kivy.properties import StringProperty

Builder.load_file(os.path.join(os.path.dirname(__file__), 'buttons.kv'))


class HeaderButton(ActionButton):
    pass

class MenuButton(Button):
    screen_name = StringProperty()