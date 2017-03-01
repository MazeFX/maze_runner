__author__ = 'MazeFX'
#!/usr/bin/kivy

# TODO - Clean up file

import os.path
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.resources import resource_find
from buttons import MenuButton

Builder.load_file(os.path.join(os.path.dirname(__file__), 'drawer.kv'))


class AppDrawer(GridLayout):

    show_drawer = BooleanProperty(False)

    drawer_header = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super(AppDrawer, self).__init__(**kwargs)

    def load_user(self, user, button_list):
        profile_name = user.profile.name
        file_name = 'avatar_' + string_to_image_name(profile_name)
        avatar = resource_find(file_name)
        self.drawer_header.header_profile.text = profile_name
        print('user= ', user.name)
        print('user last= ', user.name_last)
        full_name = user.name + ' ' + user.name_last
        self.drawer_header.header_name.text = full_name
        self.drawer_header.header_email.text = user.e_mail
        self.drawer_header.header_image.source = avatar

        for button in button_list:
            menu_button = MenuButton()
            menu_button.screen_name = button
            menu_button.text = self.app.ui_text_lib[button]
            self.ids._main_menu_buttons.add_widget(menu_button)

class DrawerHeader(RelativeLayout):

    header_image = ObjectProperty(None)

    header_profile = ObjectProperty(None)

    header_name = ObjectProperty(None)

    header_email = ObjectProperty(None)
