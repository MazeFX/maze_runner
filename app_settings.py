__author__ = 'MazeFX'
#!/usr/bin/kivy

# TODO - Clean up file

import os
import os.path
import shutil
import sys

from distutils.spawn import find_executable
from pygments import styles

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.config import ConfigParser
from kivy.uix.settings import Settings

APP_CONFIG_FILE_NAME = 'config.ini'


# monkey backport! (https://github.com/kivy/kivy/pull/2288)
if not hasattr(ConfigParser, 'upgrade'):
    try:
        from ConfigParser import ConfigParser as PythonConfigParser
    except ImportError:
        from configparser import RawConfigParser as PythonConfigParser

    def upgrade(self, default_config_file):
        '''Upgrade the configuration based on a new default config file.
        '''
        pcp = PythonConfigParser()
        pcp.read(default_config_file)
        for section in pcp.sections():
            self.setdefaults(section, dict(pcp.items(section)))
        self.write()

    ConfigParser.upgrade = upgrade


class AppSettings(Settings):
    '''Subclass of :class:`kivy.uix.settings.Settings` responsible for
       showing settings of Kivy Designer.
    '''

    config_parser = ObjectProperty(None)
    '''Config Parser for this class. Instance
       of :class:`kivy.config.ConfigParser`
    '''

    def __init__(self, **kwargs):
        super(AppSettings, self).__init__(*kwargs)
        self.app = App.get_running_app()

    def pre_load_settings(self):
        '''This function loads project settings
        '''
        self.config_parser = ConfigParser(name='App Settings')
        APP_CONFIG = os.path.join(self.app.dir,
                                       APP_CONFIG_FILE_NAME)

        _dir = self.app.dir

        DEFAULT_CONFIG = os.path.join(_dir, APP_CONFIG_FILE_NAME)
        if not os.path.exists(APP_CONFIG):
            shutil.copyfile(DEFAULT_CONFIG,
                            APP_CONFIG)

        self.config_parser.read(APP_CONFIG)
        self.config_parser.upgrade(DEFAULT_CONFIG)

    def load_settings(self):

        _dir_json = os.path.join(self.app.dir, 'settings')
        # creates a panel before insert it to update code input theme list
        panel = self.create_json_panel('App Settings',
                                        self.config_parser,
                            os.path.join(_dir_json, 'app_settings.json'))
        uid = panel.uid
        if self.interface is not None:
            self.interface.add_panel(panel, 'Kivy Designer Settings', uid)




    def on_config_change(self, *args):
        '''This function is default handler of on_config_change event.
        '''
        self.config_parser.write()
        super(AppSettings, self).on_config_change(*args)
