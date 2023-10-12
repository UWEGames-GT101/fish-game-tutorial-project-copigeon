import random
import pyasge
from gamedata import GameData


def isInside(sprite, mouse_x, mouse_y) -> bool:
    #grab the sprites bounding box, the box has 4 vertices
    bounds = sprite.getWorldBounds()
    # check to see if mouse position falls within the x and y bounds
    if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
        return True
    return False

class MyASGEGame(pyasge.ASGEGame):
    """
    The main game class
    """

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.

        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)

        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # set the game to the menu
        self.menu = True
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0

        # loads background sprite into variable and calls the background function
        self.data.background = pyasge.Sprite()
        self.initBackground()

        # defines menu text variable within the self and sets it to nothing calls the menu function
        self.menu_text = None
        self.initMenu()

        # defines the scoreboard variable sets to nothing and calls the function
        self.scoreboard = None
        self.initScoreboard()

        # loads the sprite into fish variable and calls the initFish function
        self.fish = pyasge.Sprite()
        self.initFish()

    def initBackground(self) -> bool:
        if self.data.background.loadTexture("/data/images/background.png"):
            # loaded, so make sure this is rendered first
            self.data.background.z_order = -100
            return True
        else:
            return False

    def initFish(self) -> bool:
        if (self.fish.loadTexture):
            random_fish = random.randrange(1, 7)
            if random_fish == 1:
                self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_073.png")
            elif random_fish == 2:
                self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_074.png")
            elif random_fish == 3:
                self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_076.png")
            elif random_fish == 4:
                self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_078.png")
            elif random_fish == 5:
                self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_080.png")
            elif random_fish == 6:
                self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_100.png")
            else:
                self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_102.png")

            fish_direction = random.randrange(1, 2)
            if fish_direction == 1:
                
            else:
                pass


            self.fish.z_order = 1
            self.fish.scale  = random.randrange(1, 3)
            self.spawn()
            return True
        return False

    def initScoreboard(self) -> None:
        self.scoreboard = pyasge.Text(self.data.fonts["MainFont"])
        self.scoreboard.x = 1300
        self.scoreboard.y = 75
        self.scoreboard.string = str(self.data.score).zfill(6)

    def initMenu(self) -> bool:
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "The Fantastic Fish Fiesta"
        self.menu_text.position = [100, 100]
        self.menu_text.colour = pyasge.COLOURS.HOTPINK

        # The option starts the game
        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = "Play!"
        self.play_option.position = [100, 400]
        self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        # The option starts the game
        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = "Quit!"
        self.exit_option.position = [500, 400]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        return True

    def clickHandler(self, event: pyasge.ClickEvent) -> None:
        # look to see if mouse button pressed
        if event.action == pyasge.MOUSE.BUTTON_PRESSED and \
            event.button == pyasge.MOUSE.MOUSE_BTN1:

            # is the mouse position within sprite
            if isInside (self.fish, event.x, event.y):
                self.data.score += 1 #add 1 to score
                self.scoreboard.string = str(self.data.score).zfill(6)
                self.initFish()
                self.spawn() #spawn fish

    def keyHandler(self, event: pyasge.KeyEvent) -> None:

        #Only act when the Key is pressed and not released
        if event.action == pyasge.KEYS.KEY_PRESSED:

            #Use both the right and left keys to select the play/quit options
            if event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 1:
                    self.play_option.string = ">Play!"
                    self.play_option.colour = pyasge.COLOURS.HOTPINK
                    self.exit_option.string = "Quit!"
                    self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    self.menu_option = 0
            elif event.key == pyasge.KEYS.KEY_RIGHT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 1:
                        self.play_option.string = "Play!"
                        self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                        self.exit_option.string = ">Quit!"
                        self.exit_option.colour = pyasge.COLOURS.HOTPINK
                        self.menu_option = 0

        #if enter key pressed action the menu
        if event.key == pyasge.KEYS.KEY_ENTER:
            if self.menu_option == 0:
                self.menu = False
            else:
                self.signalExit()

        # if R spawn fish
        if event.key == pyasge.KEYS.KEY_R:
            self.initFish()

    def spawn(self) -> None:
        self.fish.scale = random.randrange(1, 3)
        x = random.randint(0, self.data.game_res[0] - (self.fish.width * self.fish.scale))
        y = random.randint(0, self.data.game_res[1] - (self.fish.height * self.fish.scale))

        self.fish.x = x
        self.fish.y = y

    def update(self, game_time: pyasge.GameTime) -> None:

        if self.menu:
            # update the menu here
            pass
        else:
            # update the game here
            pass

    def render(self, game_time: pyasge.GameTime) -> None:
        """
        This is the variable time-step function. Use to update
        animations and to render the gam    e-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """

        if self.menu:
            # render the menu here
            self.data.renderer.render(self.data.background)
            self.data.renderer.render(self.menu_text)
            self.data.renderer.render(self.play_option)
            self.data.renderer.render(self.exit_option)
        else:
            # render the game here
            self.data.renderer.render(self.data.background)
            self.data.renderer.render(self.scoreboard)
            self.data.renderer.render(self.fish)
            pass


def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
