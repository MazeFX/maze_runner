__version__ = '1.0.0'
__author__ = 'MazeFX'
#!/usr/bin/kivy

# TODO - Clean up file
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ReferenceListProperty, \
    NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


class GameScreen(Screen):

    view = ObjectProperty(None)

    maze = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super(GameScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._setup)

    def _setup(self, *args):
        print('Setting up a game..')
        self.build_maze()
        self.started = False

    def build_maze(self):
        print('Building a new maze..')
        print('View size: ', self.view.size, ', screen size: ', self.size)
        self.maze = Maze()
        self.view.add_widget(self.maze)
        Clock.schedule_once(self._size)
        print('View size: ', self.view.size)

    def _size(self, *args):
        print('View size: ', self.view.size, ', screen size: ', self.size)
        self.view.size = max(self.maze.size, self.size)
        print('View size: ', self.view.size)

    def start(self):
        if not self.started:
            self.started = True
            Clock.schedule_once(self.update)

    def update(self, dt):
        finished = self.maze.update()
        if self.started and not finished:
            self.started = True
            Clock.schedule_once(self.update, 1/30)
        else:
            self.started = False


class Maze(GridLayout):

    grid = ListProperty()

    rows = NumericProperty()

    columns = NumericProperty()

    grid_size = ReferenceListProperty(rows, columns)

    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super(Maze, self).__init__(**kwargs)
        self.rows = 10
        self.columns = 10
        self.cols = self.columns
        self.width = self.rows * dp(56)
        self.height = self.columns * dp(56)
        self.current = None
        for row in range(self.rows):
            row_list = []
            for column in range(self.columns):
                tile = Tile(grid_xy=(column, row), maze=self)
                row_list.append(tile)
                self.add_widget(tile)
            self.grid.append(row_list)

        for row in self.grid:
            for tile in row:
                tile.neighborize(self.grid)

        self.current = self.grid[0][0]
        self.current.makeactive(None)

    def update(self, *args):
        finished = self.current.makecheck()
        if finished:
            return True


class Tile(RelativeLayout):

    maze = ObjectProperty(None)

    grid_x = NumericProperty()

    grid_y = NumericProperty()

    grid_xy = ReferenceListProperty(grid_x, grid_y)

    tile_bg = StringProperty()

    u_wall = ObjectProperty(None)

    d_wall = ObjectProperty(None)

    l_wall = ObjectProperty(None)

    r_wall = ObjectProperty(None)

    flag_routed = BooleanProperty(False)

    flag_down_blocked = BooleanProperty(True)
    flag_left_blocked = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super(Tile, self).__init__(**kwargs)

        self.flag_open = True

        self.u_nb = None
        self.d_nb = None
        self.l_nb = None
        self.r_nb = None
        self.tile_prior = None

        self.tile_bg = 'data/image/tile_bg_0.png'
        self.u_wall.source = 'atlas://data/image/walls/u_wall_{}'.format(int(random.randrange(4)))
        self.d_wall.source = 'atlas://data/image/walls/d_wall_{}'.format(int(random.randrange(4)))
        self.l_wall.source = 'atlas://data/image/walls/l_wall_{}'.format(int(random.randrange(4)))
        self.r_wall.source = 'atlas://data/image/walls/r_wall_{}'.format(int(random.randrange(4)))

    def neighborize(self, tile_list):
        print('Welcome to the neighborhood: Tile, ', self.grid_xy)

        if (self.maze.columns - 1) > self.grid_x:
            self.r_nb = tile_list[self.grid_y][self.grid_x + 1]
            print('greeting right neighbor: Tile, ', self.r_nb.grid_xy)
            self.r_nb.bind(flag_left_blocked=self.r_wall.setter('blocked'))
        if self.grid_x > 0:
            self.l_nb = tile_list[self.grid_y][self.grid_x - 1]
            print('greeting left neighbor: Tile, ', self.l_nb.grid_xy)
        if (self.maze.rows - 1) > self.grid_y:
            self.d_nb = tile_list[self.grid_y + 1][self.grid_x]
            print('greeting upper neighbor: Tile, ', self.d_nb.grid_xy)
        if self.grid_y > 0:
            self.u_nb = tile_list[self.grid_y - 1][self.grid_x]
            print('greeting under neighbor: Tile, ', self.u_nb.grid_xy)
            self.u_nb.bind(flag_down_blocked=self.u_wall.setter('blocked'))

        self.bind(flag_left_blocked=self.l_wall.setter('blocked'))
        self.bind(flag_down_blocked=self.d_wall.setter('blocked'))

    def makeactive(self, tile):
        self.flag_open = False
        self.flag_routed = True
        self.maze.current = self
        if tile is not None:
            self.tile_prior = tile

    def makecheck(self):
        if self == self.maze.current:
            nb_available = self.flag_open
            if self.r_nb is not None:
                nb_available |= self.r_nb.flag_open
            if self.l_nb is not None:
                nb_available |= self.l_nb.flag_open
            if self.u_nb is not None:
                nb_available |= self.u_nb.flag_open
            if self.d_nb is not None:
                nb_available |= self.d_nb.flag_open

            if nb_available:
                nb_picked = False
                while not nb_picked:
                    v = int(random.randrange(4))
                    for case in Switch(v):
                        if case(0):
                            if self.l_nb is not None:
                                if self.l_nb.flag_open:
                                    self.l_nb.makeactive(self)
                                    self.flag_left_blocked = False
                                    nb_picked = True
                                    break
                        if case(1):
                            if self.r_nb is not None:
                                if self.r_nb.flag_open:
                                    self.r_nb.makeactive(self)
                                    self.r_nb.flag_left_blocked = False
                                    nb_picked = True
                                    break
                        if case(2):
                            if self.u_nb is not None:
                                if self.u_nb.flag_open:
                                    self.u_nb.makeactive(self)
                                    self.u_nb.flag_down_blocked = False
                                    nb_picked = True
                                    break
                        if case(3):
                            if self.d_nb is not None:
                                if self.d_nb.flag_open:
                                    self.d_nb.makeactive(self)
                                    self.flag_down_blocked = False
                                    nb_picked = True
                                    break

            else:
                self.flag_routed = False
                if self.tile_prior is not None:
                    self.tile_prior.makeactive(None)
                    self.tile_prior = None
                else:
                    print('Finished')
                    return True


class MyImage(Image):

    blocked = BooleanProperty(True)


class Switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
