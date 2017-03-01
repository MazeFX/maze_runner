__version__ = '0.0.1'
__author__ = 'MazeFX'
__all__ = ('SpreadITApp', )
#!/usr/bin/kivy

import kivy
import os.path
import traceback
from os.path import dirname, join


from kivy.app import App
from kivy.animation import Animation
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty,DictProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import RiseInTransition
from kivy.utils import get_color_from_hex

from app_settings import AppSettings
from dialog import ConfirmationDialog

kivy.require('1.9.0')


class Shell(FloatLayout):
    actionbar = ObjectProperty(None)
    '''Reference to the :class:`~kivy.actionbar.ActionBar` instance.
       ActionBar is used as a MenuBar to display bunch of menu items.
       :data:`actionbar` is a :class:`~kivy.properties.ObjectProperty`
    '''

    app_content = ObjectProperty(None)
    '''Reference to
       :class:`~spread_it.screens.Spread_it_content.SpreadITContent` instance.
       :data:`designer_content` is a :class:`~kivy.properties.ObjectProperty`
    '''

    app_drawer = ObjectProperty(None)
    '''Reference to
       :class:`~spread_it.uix.drawer.SpreadITDrawer` instance.
       :data:`designer_content` is a :class:`~kivy.properties.ObjectProperty`
    '''

    statusbar = ObjectProperty(None)
    '''Reference to the :class:`~spreadit.uix.statusbar.StatusBar` instance.
       :data:`statusbar` is a :class:`~kivy.properties.ObjectProperty`
    '''

    app_settings = ObjectProperty(None)
    '''Reference of :class:`~designer.designer_settings.DesignerSettings`.
       :data:`designer_settings` is a :class:`~kivy.properties.ObjectProperty`
    '''



    def __init__(self, **kwargs):
        super(Shell, self).__init__(**kwargs)
        self.screens = {}
        self.available_screens = []
        self.active_user = None
        self.app = App.get_running_app()
        self.dir = App.get_running_app().root
        Window.bind(on_request_close=self.on_request_close)

    def setup(self):
        self.app_settings.bind(on_close=self._cancel_popup)
        self.available_screens = ['Game']
        self.screen_names = self.available_screens
        self.curdir = dirname(__file__)
        self.available_screens = [join(self.curdir,
            '{}.kv'.format(fn)) for fn in self.available_screens]

        self.actionbar.app_content = self.app_content

        #self.spread_it_drawer.load_user(self.active_user, self.screen_names)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index].lower())
        self.screens[index] = screen
        return screen

    def go_screen(self, idx):
        if self.app_content.current == self.screen_names[idx]:
            return
        self.index = idx
        self.app_content.switch_to(self.load_screen(idx), transition=RiseInTransition())

    def on_statusbar_height(self, *args):
        '''Callback for statusbar.height
        '''

        self.app_content.y = self.statusbar.height
        self.on_height(*args)

    def on_actionbar_height(self, *args):
        '''Callback for actionbar.height
        '''

        self.on_height(*args)

    def on_height(self, *args):
        '''Callback for self.height
        '''

        if self.actionbar and self.statusbar:
            self.app_content.height = self.height - self.actionbar.height - self.statusbar.height

            self.app_content.y = self.statusbar.height

    def on_request_close(self, *args):
        '''Event Handler for 'on_request_close' event of Window.
           Check if the project was saved before exit
        '''
        self._confirm_dlg = ConfirmationDialog('Quitting application,\n'
                                               'Do you want to save current session?')
        self._confirm_dlg.bind(on_save=self._perform_save_session,
                               on_ok=self._perform_quit,
                               on_cancel=self._cancel_popup)

        self._popup = Popup(title='Quit', content=self._confirm_dlg,
                            size_hint=(None, None), size=('300pt', '150pt'),
                            auto_dismiss=False)
        self._popup.open()
        return True

    def toggle_drawer(self):
        self.app_drawer.show_drawer = not self.app_drawer.show_drawer
        if self.app_drawer.show_drawer:
            x = 0
        else:
            x = 0 - self.width * .3

        Animation(pos=(x,0), d=.3, t='out_quart').start(self.app_drawer)

    @property
    def save_window_size(self):
        '''Save window size on exit.
        '''
        return bool(int(self.app_settings.config_parser.getdefault(
            'desktop', 'save_window_size', 1
        ))) if Config.getboolean('kivy', 'desktop') else False

    def _write_window_size(self, *_):
        '''Write updated window size to config
        '''
        self.app_settings.config_parser.set(
            'internal', 'window_width', Window.size[0]
        )
        self.app_settings.config_parser.set(
            'internal', 'window_height', Window.size[1]
        )
        self.app_settings.config_parser.write()

    def set_escape_exit(self):
        Config.set('kivy', 'exit_on_escape',
                   int(self.app_settings.config_parser.getdefault(
                       'desktop', 'exit_on_escape', 0)))

    def action_btn_settings_pressed(self, *args):
        '''Event handler for 'on_release' event of
           DesignerActionButton "Settings"
        '''

        self.app_settings.parent = None
        self._popup = Popup(title="Kivy Designer Settings",
                            content=self.app_settings,
                            size_hint=(None, None),
                            size=(720, 480), auto_dismiss=False)

        self._popup.open()

    def _cancel_popup(self, *args):
        '''EventHandler for all self._popup when self._popup.content
           emits 'on_cancel' or equivalent.
        '''
        self._popup.dismiss()

    def _perform_save_session(self, *args):
        print('Saving current session for user: ', self.active_user.name)
        self._perform_quit()

    def _perform_quit(self, *args):
        '''Perform Application qui.Application
        '''
        App.get_running_app().stop()


class MazeApp(App):

    started = BooleanProperty(False)
    '''Indicates if has finished the build()
    '''

    app_settings = ObjectProperty(None)
    '''Reference of :class:`~designer.designer_settings.DesignerSettings`.
       :data:`designer_settings` is a :class:`~kivy.properties.ObjectProperty`
    '''

    title = 'Supermarket Maze V{}'.format(__version__)

    def on_stop(self, *args):
        pass

    def on_request_close(self, *args):
        print('Requesting a close from app..')
        return False

    def build(self):
        self.bind(on_start=self.post_build_init)
        self.root = Shell()
        self.dir = os.path.join(os.path.dirname(__file__))
        self.app_settings = AppSettings()
        self.app_settings.pre_load_settings()
        self.app_settings.load_settings()
        self._setup()

    def post_build_init(self, ev):
        win = self._app_window
        win.bind(on_keyboard=self._key_handler)
        win.bind(on_request_close=self.on_request_close)

    def _key_handler(self, *args):
        key = args[1]
        # 27 is "escape" on computers
        print('key pressed: ', key)

    def _setup(self, *args):
        '''To setup the properties of different classes
        '''
        print('Setting up App environment..')
        self.root.statusbar.bind(height=self.root.on_statusbar_height)
        self.root.actionbar.bind(height=self.root.on_actionbar_height)

        self.root.app_settings = self.app_settings
        self.root.setup()


        idx = self.root.screen_names.index('Game')
        self.root.go_screen(idx)

        self.started = True

    def _cancel_popup(self, *args):
        '''EventHandler for all self._popup when self._popup.content
           emits 'on_cancel' or equivalent.
        '''

        self._popup.dismiss()