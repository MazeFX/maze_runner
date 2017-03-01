__author__ = 'MazeFX'
#!/usr/bin/kivy

# TODO - Clean up file

import os.path
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty



Builder.load_file(os.path.join(os.path.dirname(__file__), 'dialog.kv'))


class ConfirmationDialog(BoxLayout):
    '''ConfirmationDialog shows a confirmation message with two buttons
       "Yes" and "No". It may be used for confirming user about an operation.
       It emits 'on_ok' when "Yes" is pressed and 'on_cancel' when "No" is
       pressed.
    '''

    message = StringProperty('')
    '''It is the message to be shown
       :data:`message` is a :class:`~kivy.properties.StringProperty`
    '''

    __events__ = ('on_save', 'on_ok', 'on_cancel')

    def __init__(self, message):
        super(ConfirmationDialog, self).__init__()
        self.message = message

    def on_save(self, *args):
        pass

    def on_ok(self, *args):
        pass

    def on_cancel(self, *args):
        pass

