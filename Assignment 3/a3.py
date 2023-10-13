import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional

from a3_support import *
from model import *
from constants import *

WINDOW_WIDTH = INVENTORY_WIDTH + FARM_WIDTH
# PLANTS is in main as it should only be generated once.
PLANTS = dict()
for plant in Plant.__subclasses__():
    PLANTS[f"{plant().get_name().title()} Seed"] = plant
# This is just to clean up the plant variable used in generating the PLANTS
# constant.
plant = None


# Implement your classes here
class InfoBar(AbstractGrid):
    """InfoBar displays the Day, amount of money the places has and their
    energy.
    """
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """Initialises the InfoBar class.

        Initialises through the parent class AbstractGrid.

        Parameters:
            master (tk.Tk): The frame/window that InfoBar will be packed into.
        """
        super().__init__(master, dimensions=(2, 3),
                         size=(WINDOW_WIDTH, INFO_BAR_HEIGHT))

    def redraw(self, day: int, money: int, energy: int) -> None:
        """Reconfigures the text within InfoBar to display the relevant
        information.

        Loops through the grid positions (as defined by the parent class) and
        uses the annotate_position method to display the relevant text to that
        position.

        Parameters:
            day (int): The current in game day.
            money (int): How much money the player has.
            energy (int): How much energy the player has.
        """
        self.clear()
        default_text = ("Day:", "Money:", "Energy:", day, f"${money}", energy)
        index = 0
        for row in range(2):
            for col in range(3):
                attrs = [(row, col), default_text[index]]
                if row == 0:
                    attrs.append(HEADING_FONT)
                self.annotate_position(*attrs)
                index += 1


class FarmView(AbstractGrid):
    """FarmView displays the game/map to the player.

    FarmView displays the tile map, the plants and the player and is used to
    update the map whenever changes are made.
    """
    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int, int],
                 size: tuple[int, int], **kwargs) -> None:
        """Initialises the FarmView class.

        Initialises through the parent class AbstractGrid.

        Parameters:
            master (tk.Tk): The frame/window that InfoBar will be packed into.
            dimensions (tuple[int, int]): The amount of grid positions in
                FarmView. e.g. if dimensions=(4, 5) there are 4 rows and
                5 columns.
            size (tuple[int, int]): The pixel size of FarmView.
                e.g. if size=(400, 500) FarmView is 400 pixels wide and
                500 pixels tall.
        """
        super().__init__(master, dimensions=dimensions, size=size, **kwargs)
        self._image_cache = dict()
        self._c_size = self.get_cell_size()

    def redraw(self, ground: list[str], plants: dict[tuple[int, int], "Plant"],
               player_position: tuple[int, int], player_direction: str) -> None:
        """Draws the map when given `ground`, `plants`, `player position` and
        `player direction`.

        Loops through the `ground` list placing the relevant tile at each
        row/column position, during this it also takes any plants from
        `plants` and places them in the same row/column position (if the
        plant exists there). Finally, it takes the `player position` and
        `player direction` and places the player there.

        Parameters:
            ground (list[str]): An encoded list that describes the ground
                tile map.
            plants (dict[tuple[int, int], "Plant"]): A dictionary containing
                the row/column position of the plant (tuple[int, int]) as
                well as the plant object.
            player_position (tuple[int, int]): The row/column position of the
                player.
            player_direction (str): The facing direction of the player,
            e.g. "n", "s", "e", "w"
        """
        self.clear()

        for row_i, row in enumerate(ground):
            for col_i, cell in enumerate(row):
                # Gets the middle of each cell, otherwise the image will be
                # placed in the top left corner of each cell.
                middle = self.get_midpoint((row_i, col_i))
                tile_image = get_image(f"images/{IMAGES[cell]}",
                                       self._c_size, self._image_cache)
                self.create_image(*middle, image=tile_image)

                plant = plants.get((row_i, col_i))
                if plant is not None:
                    plant_image = get_image(
                        f"images/{get_plant_image_name(plant)}",
                        self._c_size, self._image_cache)
                    self.create_image(*middle, image=plant_image)

        player_image = get_image(f"images/{IMAGES[player_direction]}",
                                 self._c_size, self._image_cache)
        player_image_pos = self.get_midpoint(player_position)
        self.create_image(*player_image_pos, image=player_image)


class ItemView(tk.Frame):
    """ItemView displays the items the player has and/or can purchase.
    """
    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """Initialises the FarmView class.

        Initialises through the parent class tk.Frame. Adds in three Labels,
        two buttons and binds the left mouse click to ItemView (and the
        labels/frames within ItemView). Then ItemView configures the labels
        and frames to have the relevant background colours () as well as
        initialising the amount of the ItemView to whatever the player has in
        their inventory at the start of the game.

        Parameters:
            master (tk.Frame): The frame that the ItemView is to be packed into.
            item_name (str): The name of the item.
            amount (int): The amount of the item the user has.
            select_command (Optional[Callable[[str], None]]): The command to
                select the item when ItemView is clicked on.
            sell_command (Optional[Callable[[str], None]]): The command to sell
                the item (if the item can be sold).
            buy_command (Optional[Callable[[str], None]]): The command to buy
                the item (if the item can be bought).
        """
        super().__init__(master, relief="raised", borderwidth=2)
        self._item_name = item_name
        self._description_frame = tk.Frame(self)
        self._description_frame.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)

        buy_price = BUY_PRICES.get(self._item_name, "N/A")
        sell_price = SELL_PRICES.get(self._item_name, "N/A")

        # Sets up the labels within ItemView as well as packing them.
        self._item_label = tk.Label(self._description_frame,
                                    text=f"{self._item_name}: {amount}")
        self._item_buy = tk.Label(self._description_frame,
                                  text=f"Buy price: ${buy_price}")
        self._item_sell = tk.Label(self._description_frame,
                                   text=f"Sell price: ${sell_price}")
        self._item_label.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        self._item_sell.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        self._item_buy.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)

        # Sets up the buttons within ItemView as well as packing them.
        self._sell_button = tk.Button(self, text="Sell",
                                      command=lambda: sell_command(
                                          self._item_name))

        if item_name in BUY_PRICES:
            self._buy_button = tk.Button(self, text="Buy",
                                         command=lambda: buy_command(
                                             self._item_name))
            self._buy_button.pack(side=tk.LEFT, expand=tk.TRUE, padx=5, ipadx=5)
        self._sell_button.pack(side=tk.LEFT, expand=tk.TRUE, padx=5, ipadx=5)

        # List containing all "top level" widgets - Widgets that the user is
        # able to click on that should have a conditional background colour
        # as well as a binding to the left mouse button event.
        self._widgets = [self, self._description_frame, self._item_label,
                         self._item_sell, self._item_buy]

        bg_color = (INVENTORY_COLOUR if amount > 0 else INVENTORY_EMPTY_COLOUR)
        for widget in self._widgets:
            widget.configure(
                bg=bg_color
            )
            widget.bind("<Button-1>",
                        lambda _: select_command(self._item_name))

    def update(self, amount: int, selected: bool = False) -> None:
        """Updates the ItemView object to have the relevant amount and colour
        (colour defined by amount and if the item is selected).

        Loops through the widgets (as defined in __init__ under
        `self._widgets`) and changes their background colour to match the
        amount of that item the user has as well as if it's selected. if the
        user has > 0 of that item the colour is `INVENTORY_COLOUR`, if the
        user has < 0 of that item the colour is `INVENTORY_EMPTY_COLOUR` and if
        the item is selected and amount > 0 the colour is
        `INVENTORY_SELECTED_COLOUR`

        Parameters:
            amount (int): The amount of the item the player has.
            selected (bool): If the item is selected or not.
        """
        self._item_label.configure(
            text=f"{self._item_name}: {amount}"
        )
        colour = INVENTORY_EMPTY_COLOUR
        if selected:
            colour = INVENTORY_SELECTED_COLOUR
        elif amount > 0:
            colour = INVENTORY_COLOUR
        if selected and amount == 0:
            colour = INVENTORY_EMPTY_COLOUR

        for widget in self._widgets:
            widget.configure(
                bg=colour
            )


class FarmGame:
    """FarmGame handles all keyboard interaction as well as initial setup and
    causes any visual updates to occur through the ItemView, FarmView and
    InfoBar classes.
    """
    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """Initialises the FarmGame class.

        Calls the ItemView, FarmView and InfoBar classes to construct the
        game view as well as setting up the player control key bindings. Also
        causes all visual updates to occur on player interaction.

        Parameters:
            master (tk.Tk): The main tkinter window.
            map_file (str): The path to the map file.
        """
        self._item_views = dict()
        self._title_banner_image = get_image(image_name="images/header.png",
                                             size=(WINDOW_WIDTH, BANNER_HEIGHT))
        title_banner = tk.Label(master, image=self._title_banner_image)
        title_banner.pack(side=tk.TOP, anchor=tk.N)
        master.title("Farm Game")

        master.bind("<KeyPress>", self.handle_keypress)

        self._main_game_window = tk.Frame(master)
        self._main_game_window.pack(side=tk.TOP)

        self._farm_engine = FarmModel(map_file)
        self._player = self._farm_engine.get_player

        size = (FARM_WIDTH, FARM_WIDTH)
        self._farm_view = FarmView(self._main_game_window,
                                   self._farm_engine.get_dimensions(),
                                   size)
        self._farm_view.pack(side=tk.LEFT)

        for item in ITEMS:
            i_view = ItemView(self._main_game_window, item,
                              self._player(
                              ).get_inventory().get(item, 0),
                              self.select_item,
                              self.sell_item,
                              self.buy_item)
            i_view.pack(
                side=tk.TOP,
                expand=tk.TRUE,
                fill=tk.BOTH
            )
            self._item_views[item] = i_view

        self._info_bar = InfoBar(master)
        self._info_bar.pack(side=tk.TOP)

        next_day_button = tk.Button(master, text="Next day",
                                    command=self._next_day_event)
        next_day_button.pack(side=tk.TOP, anchor=tk.N)
        self.redraw()

    def _next_day_event(self):
        """Runs all needed functions for the next day event

        Runs the models new_day method as well as the redraw method.
        """
        self._farm_engine.new_day()
        self.redraw()

    def redraw(self) -> None:
        """Redraws all the view classes with relevant info.

        Redraws FarmView, InfoBar and all ItemViews.
        """
        self._farm_view.redraw(
            self._farm_engine.get_map(),
            self._farm_engine.get_plants(),
            self._farm_engine.get_player_position(),
            self._farm_engine.get_player_direction()
        )
        self._info_bar.redraw(
            self._farm_engine.get_days_elapsed(),
            self._player().get_money(),
            self._player().get_energy()
        )
        for item in ITEMS:
            self._item_views[item].update(
                self._player().get_inventory().get(item, 0),
                selected=(
                    True if item == self._player().get_selected_item()
                    else False)
            )

    def handle_keypress(self, event: tk.Event) -> None:
        """Handles all keypress events from the user.

         Handles all valid key presses and performs the appropriate actions
         as well as redrawing the game.

        Parameters:
            event (tk.Event): The keypress event.
        """
        allowed_keys = "wasdphrtu"
        key = event.keysym
        if key not in allowed_keys:
            return

        player_position = self._farm_engine.get_player_position()
        plant_positions = self._farm_engine.get_plants()
        plant_at_player = plant_positions.get(player_position, None)
        selected_item = (item if (item := self._player(
        ).get_selected_item()) is not None else None)
        game_map = self._farm_engine.get_map()

        if key in "wasd":
            self._farm_engine.move_player(key)
        if key == "t":
            self._farm_engine.till_soil(player_position)
        elif key == "u":
            if plant_at_player is None:
                self._farm_engine.untill_soil(player_position)
        elif (
                key == "p" and
                game_map[player_position[0]][player_position[1]] == SOIL and
                plant_at_player is None and
                selected_item in SEEDS and
                selected_item in self._player().get_inventory()
        ):
            self._farm_engine.add_plant(player_position,
                                        PLANTS[selected_item]()
                                        )
            self._player().remove_item((selected_item, 1))
        elif (
                key in "hr" and
                plant_at_player is not None
        ):
            if plant_at_player is not None and plant_at_player.can_harvest():
                item = self._farm_engine.harvest_plant(player_position)
                self._player().add_item(item)
            elif key == "r":
                self._farm_engine.remove_plant(player_position)

        self.redraw()

    def select_item(self, item_name: str) -> None:
        """Sets the selected item in the model and visually shows the selected
        item by highlighting it.

        Changes the selected item then redraws the screen.

        Parameters:
            item_name (str): The name of the selected item.
        """
        self._player().select_item(item_name)
        self.redraw()

    def buy_item(self, item_name: str) -> None:
        """Buy the item and redraw the screen."""
        price = BUY_PRICES[item_name]
        self._player().buy(item_name, price)
        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """Sell the item and redraw the screen."""
        price = SELL_PRICES[item_name]
        self._player().sell(item_name, price)
        self.redraw()


def play_game(root: tk.Tk, map_file: str) -> None:
    """Starts the game."""
    FarmGame(root, map_file)
    root.mainloop()


def main() -> None:
    """Creates the root object and passes it to play_game."""
    root = tk.Tk()
    play_game(root, "maps/map2.txt")


if __name__ == '__main__':
    main()
