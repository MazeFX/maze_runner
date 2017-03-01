__version__ = '1.0.0'
__author__ = 'MazeFX'
#!/usr/bin/kivy

# TODO - Clean up file

if __name__ == '__main__':
    from kivy.config import Config
    Config.set('graphics', 'width', '1000')
    Config.set('graphics', 'height', '1000')
    import os.path
    from mazeapp import MazeApp
    from kivy.resources import resource_add_path
    from kivy.core.text import LabelBase

    resource_add_path(os.path.join(os.path.dirname(__file__), 'data'))
    resource_add_path(os.path.join(os.path.dirname(__file__), 'data', 'image'))
    resource_add_path(os.path.join(os.path.dirname(__file__), 'data', 'icons'))
    LabelBase.register(name='Pictograms',
                       fn_regular=os.path.join(os.path.dirname(__file__), 'data', 'fonts', 'modernpics.ttf'))
    MazeApp().run()