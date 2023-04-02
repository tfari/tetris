""" Pre-testing concepts
    Simple grid-based visualizer for shape rotations, as well as the building blocks for the architecture.

"""
import os
import json
import random
from typing import Optional
from dataclasses import dataclass, asdict

import pygame


# GLOBAL PATHS
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = SCRIPT_PATH + '/data'
SETTINGS_FILEPATH = DATA_PATH + '/settings.json'


@dataclass()
class EditableSettings:
    """ User-editable settings, exist in a file under DATA_PATH/SETTINGS_FILEPATH """
    grid_lines_color: tuple[int, int, int] = (55, 55, 55)
    empty_block_color: tuple[int, int, int] = (35, 35, 35)

    shape_1_color: tuple[int, int, int] = (107, 216, 223)
    shape_2_color: tuple[int, int, int] = (222, 111, 106)
    shape_3_color: tuple[int, int, int] = (222, 183, 84)
    shape_4_color: tuple[int, int, int] = (109, 139, 222)
    shape_5_color: tuple[int, int, int] = (95, 222, 141)
    shape_6_color: tuple[int, int, int] = (216, 126, 222)
    shape_7_color: tuple[int, int, int] = (223, 143, 93)

    @staticmethod  # TODO 3: (https://www.digitalocean.com/community/tutorials/python-static-method)
    def load_editable_settings():
        """ Load editable settings from DATA_PATH/SETTINGS_FILEPATH file. If no file is there, create one with the
        default values. """
        # TODO 4: Complete this method.
        try:
            with open(SETTINGS_FILEPATH, 'r', encoding='utf-8') as r_file:
                data = json.load(r_file)
            # TODO 4.1 : Here we create an instance of EditableSettings with the contents of settings_data,
            #  and return it.
        except FileNotFoundError:
            print(f"Settings file not found at: {SETTINGS_FILEPATH}. Creating a new one with default values...")
            # TODO 4.2: Here we create an instance of EditableSettings with no arguments, save that as a file,
            #  and then return it. Use an indent of 4 when saving the json file. We will use the dunder variable
            #  __dict__ for it. (https://www.pythonmorsels.com/dunder-variables/) Notice that our approach does not
            #  work if we do not use type hinting for the variables we define in this class.
            es = EditableSettings()
        except (json.decoder.JSONDecodeError, TypeError) as e:
            # TODO 4.3 : Here we will do the same as in 4.2. If you want, save a step and make both 4.2 and 4.3
            #  return the result from a function, say, "__make_default()" that does what 4.2 says.


@dataclass()  # TODO 2: https://docs.python.org/3/library/dataclasses.html
class Settings:
    """ Global, hard-coded, settings for the application """
    app_title = 'SHAPE VISUALIZER'
    window_size = (400, 400)  # (X, Y)
    grid_size = (4, 4)

    fps_limit = 60

    editables = EditableSettings.load_editable_settings()

    # TODO 5: You need to set up the "shape" and "rotation_mods" for the rest of the shapes here. I've left a comment
    #  of the first line of each shape showing what shape it is. "shape" is a list of (x, y) positions for each
    #  square of the shape. "rotation_mods" is a list of lists of (x, y) modifications that need to be applied on
    #  each square in order to produce the correct rotated shape for each rotation (90°, 180°, 270°, 360°). Same
    #  shapes can be resolved by rotating only twice, or in the case of the square (::), by one. In the case of
    #  "shape" we will take the left-most square to be X=1 (except for the line (....) shape, and the top-most square
    #  to be Y=0. For the case of rotations you might want to use the same pivot point, say shape[1] in the case of the
    #  line (notice its rotation_mods is always (0, 0)), to make rotations be consistent. Check it in the visualizer as
    #  you go.
    #  This step is not really the 5th one, it is one that you should probably return to after completing the rest of
    #  the project, in order to fine-tune everything to look nice and consistent among the shapes.

    shapes = [  # Except for the .... shape, all others should have the left-most square at X=1, and top-most at Y=0.
        {'shape': [(0, 0), (1, 0), (2, 0), (3, 0)],  # ....
         'rotation_mods': [
             [(1, -1), (0, 0), (-1, 1), (-2, 2)],
             [(-1, 1), (0, 0), (1, -1), (2, -2)]
         ],
         'color': editables.shape_1_color},

        # {'shape': [],  # ::
        #  'rotation_mods': [
        #  ],
        #  'color': editables.shape_2_color},
        #
        # {'shape': [],  # .:.
        #  'rotation_mods': [
        #  ],
        #  'color': editables.shape_3_color},
        #
        # {'shape': [],  # :..
        #  'rotation_mods': [
        #  ],
        #  'color': editables.shape_4_color},
        #
        # {'shape': [],  # ..:
        #  'rotation_mods': [
        #  ],
        #  'color': editables.shape_5_color},
        #
        # {'shape': [],  # °:.
        #  'rotation_mods': [
        #  ],
        #  'color': editables.shape_6_color},
        #
        # {'shape': [],  # .:°
        #  'rotation_mods': [
        #  ],
        #  'color': editables.shape_7_color}
    ]


class BlockSurface:
    """ Surface for blocks """
    def __init__(self, primary_color: tuple[int, int, int], square_size: tuple[int, int], *, pretty: bool = True):
        # TODO 10: Notice in this __init__ signature there are two things you might not have seen yet: ",*,
        #  " and the "pretty:bool = True". The first one means that "from here on, the rest of the arguments are
        #  KEYWORD only. This means that if we want to set pretty, we need to do __init__(bla, bla, bla,
        #  pretty=False) or pretty=True). It means that this argument can only be passed by explicitely using the
        #  keyword=value syntax. The second thing, "pretty:bool = True". Means that this parameter does not need to
        #  be passed, the "= True" means that "if this paramater is not passed, use the default value of True". All
        #  of this basically means: "When creating a BlockSurface object, unless pretty is passed, set pretty as
        #  True. If pretty is passed, enforce that is passed by saying "pretty=False". This is done for the sake of
        #  readability. Because this class operates substantially different depending on the pretty value,
        #  we want to make it so that when pretty is False, it is as obvious as possible for the reader.
        self.__primary_color = primary_color
        self.__square_size = square_size
        self.__pretty = pretty


        # TODO 11: We use Optional[thing] here just to make pycharm not show this assignment to None as an error.
        #  Optional means this can be a BlockSurface or None. We do this because we want to declare self.surface on
        #  __init__, but we want to fill self.surface on initialize_block_surface(). You will see this crop up on
        #  other places, its mostly so pycharm does not mark this stuff as an error, but in most cases type hinting a
        #  variable setting is overkill.
        self.surface: Optional[pygame.Surface] = None
        self.initialize_block_surface(self.__square_size)

    def initialize_block_surface(self, square_sizes: tuple[int, int]):
        """ Draws the block surface for this kind of shape """
        self.surface = pygame.Surface(square_sizes)
        if not self.__pretty:  # Non-pretty is perfectly rectangular squares
            pygame.draw.rect(self.surface, self.__primary_color, (0, 0, square_sizes[0], square_sizes[1]))
        else:  # When pretty, we use borders
            # TODO 12: We need to set the background to empty because we are using circled borders, try it without
            #  the following statement and you will see why!
            self.surface.fill(EditableSettings.empty_block_color)
            # TODO 13: Notice we are using the class variable, but this is actually a value we get from a file. If
            #  you edit the empty_block_color in the data/settings.json file you will see this stops working! This
            #  will however make sense later, we do not want to pass the settings to this class as a parameter. We
            #  will need to find a way to make it so the settings are always globally accesible.

            # Draw the color block
            pygame.draw.rect(self.surface, self.__primary_color, (0, 0, square_sizes[0], square_sizes[1]),
                             border_radius=5)

        if self.__pretty:  # When pretty we draw some extra stuff
            # Shade coloring
            pygame.draw.rect(self.surface, self.__mod_color(self.__primary_color, -20),
                             (0, 0, square_sizes[0], square_sizes[1]), width=5, border_radius=5)
            # Highlight coloring
            offset = 7
            # TODO 15:  We use an offset because we do not want to draw over the shading, plus we are
            #  using a circled rectangle, so we cant use 0. (This will become clearer when you get the whole thing
            #  running and start playing with this values)
            pygame.draw.line(self.surface, self.__mod_color(self.__primary_color, 50),
                             (offset, offset), (offset, square_sizes[1] - offset * 2), width=5)
            pygame.draw.line(self.surface, self.__mod_color(self.__primary_color, 50),
                             (offset, offset), (square_sizes[0] - offset * 2, offset), width=5)

        # TODO 16: Notice all the times we used numbers in here. All these numbers should really be part of the
        #  settings. In essence, we want all literal numbers to exist inside settings, either in Settings,
        #  if we do not want users to change them, or in EditableSettings. However, the important part
        #  is that we do not want to have magic numbers laying around all of our code, it is better if we have them
        #  all concentrated in a single place.


    @staticmethod
    def __mod_color(color: tuple[int, int, int], mod: int) -> tuple[int, int, int]:
        """ Return a (r, g, b) tuple in which every vector is modified by mod."""
        # TODO 14: Complete this method. Remember each color vector (r,g and b) must be between 0 and 255 for the
        #  full tuple to be a valid color.

@dataclass()
class ShapeInfo:
    """ Shape information for each tetromino: https://en.wikipedia.org/wiki/Tetromino"""
    # TODO 9: Look here, we could merge this with the Shape class, but instead, by doing this, we only are holding
    #  one instance of each shape's information in memory, and when we create Shape instances, we simply hold state
    #  values in Shape, and all the common stuff of shapes in here. This shaves a few cycles from everytime we are
    #  creating a new Shape object, plus it also allows us to have a single surface for the blocks of each shape,
    #  which is probably the most important part, as drawing operations are expensive.
    shape: list[tuple[int, int]]
    rotation_mods: list[list[tuple[int, int]]]
    color: tuple[int, int, int]
    block_surface: Optional[BlockSurface] = None

    def initialize_block_surface(self, square_sizes: tuple[int, int]):
        """ Draws the block surface for this kind of shape """
        if not self.block_surface:
            self.block_surface = BlockSurface(self.color, square_sizes)
        else:
            self.block_surface.initialize_block_surface(square_sizes)


class Shape:
    """ An actual tetris shape """
    def __init__(self, shape_info: ShapeInfo):
        self.shape_info = shape_info
        self.pos = self.shape_info.shape
        self.__current_rotation_index = -1

    def calculate_mod_pos(self, mod: tuple[int, int]) -> list[tuple[int, int]]:
        """ Returns what the position of this shape would be, given a single (x, y) tuple modifier. Does not modify
         the instance position. """
        # TODO 26: Complete this method

    def calculate_next_flip_pos(self) -> list[tuple[int, int]]:
        """ Returns what the position of this shape would be in the next rotation. """
        # TODO 27: Complete this method

    def rotate(self, new_pos: list[tuple[int, int]]):
        """ Rotate the shape to new_pos (self.pos = new_pos), increment current_rotation_index accordingly """
        # TODO 28: Complete this method


class ScreenController:
    """ Controls what gets drawn on screen, as well as sizing the screen """

    def __init__(self, settings: Settings):
        self.settings = settings
        # TODO 6: Use a method on pygame.display (https://www.pygame.org/docs/ref/display.html) to set the window title to self.settings.app_title

        self.__window_size = self.settings.window_size
        self.window_surface = pygame.display.set_mode(self.__window_size)

        # TODO 7: Get the size in (X, Y) pixels that each square will have for a grid of self.settings.grid_size in a
        #  screen of size self.__window_size.
        self.square_size: tuple[int, int] = (int(), int())

        self.__update_stack = []  # This starts empty

    def add_to_update_stack(self, surface: pygame.Surface, position: tuple[int, int]) -> None:
        """ Adds a surface and a position to the update stack, to be updated on the next .update() call """
        self.__update_stack.append({'position': position, 'surface': surface})

    def update(self):
        """ Update screen depending on contents of self.__update_stack """
        positions = []
        # TODO 8: do a self.window_surface.blit operation for each element in the self.__update_stack, also save the
        #  Rects () of this blit operation in the list positions.
        self.__update_stack = []
        pygame.display.update(positions)


class MainApp:
    """ Handles game loop and input parsing """
    def __init__(self):
        self.settings = Settings()
        self.screen_controller = ScreenController(self.settings)
        self.clock = pygame.time.Clock()
        self.running = False

        # 1 - Create ShapeInfos and the Empty BlockSurface
        self.shape_infos = [ShapeInfo(*s.values()) for s in self.settings.shapes]
        self.__empty_block_surface = BlockSurface(self.settings.editables.empty_block_color,
                                                  self.screen_controller.square_size, pretty=False)

        # TODO 17: Notice what we are doing here, we created a ShapeInfo for each shape in settings,
        #  then an __empty_block_surface for empty blocks in the grid. Now we are initializing the blocks in our
        #  ShapeInfos to draw what the blocks for each shape look like.
        for si in self.shape_infos:  # Initialize ShapeInfo BlockSurfaces
            si.initialize_block_surface(self.screen_controller.square_size)

        # Initialize game_grid with all empty BlockSurfaces
        self.game_grid: list[list[BlockSurface]] = self.__get_game_grid()

        # Initialize grid surface
        self.grid_surface = self.__make_grid_surface(self.screen_controller.square_size, self.settings.grid_size,
                                                     self.settings.editables.grid_lines_color)
        self.__showing_grid = False

        # Initialize a first current_shape object
        self.current_shape: Optional[Shape] = None
        self.change_shape()

    def __get_game_grid(self) -> list[list[BlockSurface]]:
        """ Get grid of Y list of X squares """
        # TODO 18: Complete: return a list of lists of empty block surfaces

    def __call_full_screen_update(self):
        """ Full screen update. Blank screen, draw current shape, then grid if showing. """
        # Draw empty screen first
        # TODO 29: Set all squares as empty

        # Draw current shape position
        # TODO 30: Set current shape position squares on their on block surfaces


        if self.__showing_grid:
            # TODO 31: Notice this
            self.screen_controller.add_to_update_stack(self.grid_surface, (0, 0))

    @staticmethod
    def __make_grid_surface(square_size: tuple[int, int], grid_size: tuple[int, int],
                            lines_color: tuple[int, int, int], *,
                            alpha_color: tuple[int, int, int] = (0, 0, 0)) -> pygame.Surface:
        """ Make a grid surface and return it """
        w_grid_surface = pygame.surface.Surface((grid_size[0] * square_size[0], grid_size[1] * square_size[1]))

        # We make background transparent for this surface
        w_grid_surface.fill(alpha_color)
        w_grid_surface.set_colorkey(alpha_color)
        # TODO 19: Notice what we did here. We made a surface of the size of grid_size * square_size, then set the
        #  surface to "alpha_color" which we set as black (0, 0, 0) by default, and then we made black the invisible
        #  color.

        # TODO 20: Draw lines on the surface in the shape of a grid (https://www.pygame.org/docs/ref/draw.html#pygame.draw.line)

        return w_grid_surface

    def game_loop(self):
        """ Game loop """
        self.running = True
        while self.running:
            # 1 - Handle input
            self.handle_input()
            # 2 - Handle game rules
            # 3 - Update screen
            self.screen_controller.update()
            # 4 - Update sound
            # 5 - Limit clock to FPS limit
            self.clock.tick(self.settings.fps_limit)

    def handle_input(self):
        """ Handle user input """
        # TODO 22: Notice this! We could be using if-else, we are using a map to methods!
        # TODO 22.1: Fill these dictionary with the appropriate methods.
        key_up_to_methods = {
            pygame.K_UP: self.rotate_shape,
            pygame.K_RETURN:  # TODO 32: change_shape
            pygame.K_g:  # TODO 33: toggle_grid
        }
        key_down_to_methods = {}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYUP and event.key in key_up_to_methods:
                key_up_to_methods[event.key]()
            elif event.type == pygame.KEYDOWN and event.key in key_down_to_methods:
                key_down_to_methods[event.key]()

    def rotate_shape(self):
        """ Rotate the current shape """
        # TODO 23: Complete this method.

    def change_shape(self):
        """ Change current shape for a new random one. Center it as good as possible into the grid. """
        # TODO 24: Complete this method.

    def toggle_grid(self):
        """ Toggle grid on and off """
        # TODO 25: Complete this method.

    def __chose_random_shape(self) -> Shape:
        return Shape(random.choice(self.shape_infos))

    def quit(self):
        """ Quit the application """
        self.running = False


pygame.init()  # TODO 1 : Initialize pygame before starting our app (https://www.pygame.org/docs/tut/ImportInit.html)
app = MainApp()
app.game_loop()
