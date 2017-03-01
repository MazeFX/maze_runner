__author__ = 'MazeFX'
#!/usr/bin/kivy

# TODO - Clean up file

import os.path
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.actionbar import ActionBar, ActionGroup, ActionPrevious, ActionButton, \
    ActionItem, ActionView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout


Builder.load_file(os.path.join(os.path.dirname(__file__), 'actionbar.kv'))


class AppActionBar(ActionBar):

    search_mode = BooleanProperty(False)

    app_content = ObjectProperty(None)

    def toggle_search_mode(self):
        self.search_mode = not self.search_mode
        h = self.ids.search_field.size[1]
        if self.search_mode:
            self.ids.search_field.disabled = False
            self.ids.search_field.text = ''
            self.ids.search_field.focus = True
            w = dp(400)

        else:
            self.ids.search_field.disabled = True
            self.ids.search_field.text = ''
            w = 0

        Animation(size=(w, h), d=.3, t='out_quart').start(self.ids.search_field)

    def generate_maze(self, *args):
        self.app_content.current_screen.start()



class AppActionView(ActionView):
    '''Custom ActionView to support custom action group
    '''

    pass
