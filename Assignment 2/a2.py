from a2_support import *


# Implement your classes here
# Cards
class Card:
    """Parent class to all cards.

    Sets up all methods and implements default values.
    """

    def __init__(self) -> None:
        """Initialises an instance of Card.

        Usage:
            >>> card = Card()
            >>> card
            'Card()'
            >>> print(card)
            'Card: A card.'
            >>> card.get_damage_amount()
            0
        """
        self._card_attrs = {
            "id": self.__class__.__name__,
            "damage": 0,
            "block": 0,
            "cost": 1,
            "status mods": dict(),
            "requires target": True,
        }
        self._make_description()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.get_name()}: {self.get_description()}"

    def __repr__(self) -> str:
        """Returns the string representation of an instance of this object"""
        return f"{self.get_name()}()"

    def _make_description(self) -> None:
        """Makes and sets the cards description.
        """
        desc_items = ["damage", "block", "status mods"]
        flavour_text = ["Deal", "Gain", "Apply"]
        description = list()
        for index, item in enumerate(desc_items):
            value = self._card_attrs[item]

            if type(value) == int and value > 0:
                description.append(f"{flavour_text[index]} "
                                   f"{value} "
                                   f"{item}.")
            elif type(value) == dict and len(value) > 0:
                for effect_name, duration in value.items():
                    description.append(f"{flavour_text[index]} "
                                       f"{duration} "
                                       f"{effect_name}.")

        if len(description) == 0:
            self._card_attrs["description"] = "A card."
            return
        self._card_attrs["description"] = " ".join(description)

    def get_damage_amount(self) -> int:
        """Returns damage amount as an integer"""
        return self._card_attrs["damage"]

    def get_block(self) -> int:
        """Returns block as an integer"""
        return self._card_attrs["block"]

    def get_energy_cost(self) -> int:
        """Returns energy cost as an integer"""
        return self._card_attrs["cost"]

    def get_status_modifiers(self) -> dict[str, int]:
        """Returns status modifiers as a dictionary"""
        return self._card_attrs["status mods"]

    def get_name(self) -> str:
        """Returns name as a string"""
        return self._card_attrs["id"]

    def get_description(self) -> str:
        """Returns description as a string"""
        return self._card_attrs["description"]

    def requires_target(self) -> bool:
        """Returns True or False if the card requires a target"""
        return self._card_attrs["requires target"]


class Strike(Card):
    """The Strike card.
    """

    def __init__(self) -> None:
        """Initialises Strike"""
        super().__init__()
        self._card_attrs["damage"] = 6
        self._make_description()


class Defend(Card):
    """The Defend card.
    """

    def __init__(self) -> None:
        """Initialises Defend"""
        super().__init__()
        self._card_attrs["block"] = 5
        self._card_attrs["requires target"] = False
        self._make_description()


class Bash(Card):
    """The Bash card.
    """

    def __init__(self) -> None:
        """Initialises Bash"""
        super().__init__()
        self._card_attrs["damage"] = 7
        self._card_attrs["block"] = 5
        self._card_attrs["cost"] = 2
        self._make_description()


class Neutralize(Card):
    """The Neutralize card.
    """

    def __init__(self) -> None:
        """Initialises Neutralize"""
        super().__init__()
        self._card_attrs["damage"] = 3
        self._card_attrs["cost"] = 0
        self._card_attrs["status mods"] = {"weak": 1, "vulnerable": 2}
        self._make_description()


class Survivor(Card):
    """The Survivor card.
    """

    def __init__(self) -> None:
        """Initialises Survivor"""
        super().__init__()
        self._card_attrs["block"] = 8
        self._card_attrs["status mods"] = {"strength": 1}
        self._card_attrs["description"] = "Gain 8 block and 1 strength."
        self._card_attrs["requires target"] = False


# Entities
class Entity:
    """Parent class to all entities.

    Sets up basic methods for all entities and implements default values.
    """

    def __init__(self, max_hp: int) -> None:
        """Initialises an instance of Entity.

        Parameters:
             max_hp (int): Holds the maximum hp (or more accurately the
                starting hp) of the Entity.

        Usage:
            >>> entity = Entity(20)
            >>> entity.get_hp()
            20
            >>> entity.get_name()
            'Entity'
        """
        # id here is simply the name of the class/entity not the unique ID given
        # to the Monster class and subclasses.
        self._entity_attrs = {
            "id": self.__class__.__name__,
            "max hp": max_hp,
            "hp": max_hp,
            "block": 0,
            "strength": 0,
            "turns weak": 0,
            "turns vulnerable": 0,
        }

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.get_name()}: {str(self.get_hp())}/{self.get_max_hp()} HP"

    def __repr__(self):
        """Returns the string representation of an instance of this object"""
        return f"{self.get_name()}({self.get_max_hp()})"

    def get_hp(self) -> int:
        """Get current hp."""
        return self._entity_attrs["hp"]

    def get_max_hp(self) -> int:
        """Get entities max hp (initial hp)."""
        return self._entity_attrs["max hp"]

    def get_block(self) -> int:
        """Get current block."""
        return self._entity_attrs["block"]

    def get_strength(self) -> int:
        """Get current strength."""
        return self._entity_attrs["strength"]

    def get_weak(self) -> int:
        """Get the number of turns an entity is weak for."""
        return self._entity_attrs["turns weak"]

    def get_vulnerable(self) -> int:
        """Get the number of turns an entity is vulnerable for."""
        return self._entity_attrs["turns vulnerable"]

    def get_name(self) -> str:
        """Get the name of the entity"""
        return self._entity_attrs["id"]

    def reduce_hp(self, amount: int) -> None:
        """Reduces the entity's block then if block is 0 and there is still
        outstanding damage HP is reduced."""
        if amount > self.get_block():
            amount -= self.get_block()
            self._entity_attrs["block"] = 0
        else:
            self._entity_attrs["block"] -= amount
            return
        if self.get_hp() - amount < 0:
            self._entity_attrs["hp"] = 0
        else:
            self._entity_attrs["hp"] -= amount

    def is_defeated(self) -> bool:
        """Checks if entity health is 0."""
        return True if self._entity_attrs["hp"] == 0 else False

    def add_block(self, amount: int) -> None:
        """Adds block to the entity."""
        self._entity_attrs["block"] += amount

    def add_strength(self, amount: int) -> None:
        """Adds strength to the entity."""
        self._entity_attrs["strength"] += amount

    def add_weak(self, amount: int) -> None:
        """Adds weak to the entity."""
        self._entity_attrs["turns weak"] += amount

    def add_vulnerable(self, amount: int) -> None:
        """Adds vulnerable to the entity."""
        self._entity_attrs["turns vulnerable"] += amount

    def new_turn(self) -> None:
        """Default actions for all entities to take when a new turn begins."""
        turn_attrs = ["turns weak", "turns vulnerable"]
        self._entity_attrs["block"] = 0
        for attr in turn_attrs:
            if self._entity_attrs[attr] > 0:
                self._entity_attrs[attr] -= 1


class Player(Entity):
    """Parent class to all player types, also a child to Entity.

    Sets up all methods for Player classes and subclasses.
    """

    def __init__(self, max_hp: int, cards: list[Card] | None = None) -> None:
        """Initialises the Player class.

        Calls the __init__ method of the Entity class to set up basic
        functionality. Takes cards as meaning players deck so if cards is not
        None it is added to the players deck.

        Parameters:
            max_hp (int): The max (initial) hp of the player.
            cards (list[Card]): The cards to be added to the players deck.

        Usage:
            >>> cards = [Bash(), Bash(), Strike(), Defend()]
            >>> player = Player(20, cards)
            >>> player.get_deck()
            [Bash(), Bash(), Strike(), Defend()]
            >>> player.get_hp()
            20
        """
        super().__init__(max_hp=max_hp)
        self._entity_attrs["cards"] = {
            "deck": (list() if type(cards) is None else cards),
            "hand": list(),
            "discard pile": list(),
        }
        self._entity_attrs["energy"] = 3

    def __repr__(self) -> str:
        """Returns the string representation of an instance of this object"""
        if self.get_deck() is not None:
            return f"{self.get_name()}({self.get_max_hp()}, {self.get_deck()})"
        return f"{self.get_name()}({self.get_max_hp()})"

    def _get_cards(self) -> dict[str, list]:
        """Gets the dictionary stored at the key 'cards' in the entities
        attributes dictionary"""
        return self._entity_attrs["cards"]

    def _reset_cards(self, condition: None | int = None) -> None:
        """Resets the player's hand and discard pile.

        If condition is None both the player's hand and discard pile are
        emptied. Otherwise, the cards to reset can be specified.

        Parameters:
            condition (int | None): If condition is None all cards that can
                be reset are reset ^, otherwise, condition is treated as an
                index to reset one set of cards.

                ^ All cards that can be reset are: hand, discard pile.
        """
        reset_cards = ["hand", "discard pile"]
        if condition is None:
            for r_card in reset_cards:
                self._entity_attrs["cards"][r_card] = list()
        else:
            self._entity_attrs["cards"][reset_cards[condition]] = list()

    def get_energy(self) -> int:
        """Returns the player's energy."""
        return self._entity_attrs["energy"]

    def set_energy(self, energy: int) -> None:
        """Sets the player's energy to a given value.

        Parameters:
            energy (int): The value to set the player's energy to.
        """
        if type(energy) == int:
            self._entity_attrs["energy"] = energy
        else:
            raise ValueError(f"energy must be an integer, {energy=}, "
                             f"{type(energy)=}")

    def get_hand(self) -> list[Card]:
        """Gets the player's hand."""
        return self._get_cards()["hand"]

    def set_cards(self, cards: list[Card], location: int) -> None:
        """Sets the players cards at a specified location to a specific value.

        Takes cards (list) and location (int), replaces the cards at location
        with the cards specified.

        Parameters:
            cards (list[Card]): A list of the cards you want to be replacing the
                old ones.
            location (int): The "location" you want to put the cards at,
                0 is the players deck, 1 is their hand and 2 is their discard
                pile.
        """
        if type(cards) != list or (any(type(card) not in
                                       [Card] + Card.__subclasses__()
                                       for card in cards)):
            raise ValueError("cards must be a list containing only "
                             f"containing cards, {cards=}, {type(cards)=}")
        else:
            player_cards = self._entity_attrs["cards"]
            match location:
                case 0:
                    player_cards["deck"] = cards
                case 1:
                    player_cards["hand"] = cards
                case 2:
                    player_cards["discard pile"] = cards

    def get_deck(self) -> list[Card]:
        """Gets the player's deck"""
        return self._get_cards()["deck"]

    def get_discarded(self) -> list[Card]:
        """Gets the player's discard pile."""
        return self._get_cards()["discard pile"]

    def start_new_encounter(self) -> None:
        """Actions to take when an encounter starts.

        Takes the cards left in the players hand and any cards in the discard
        pile and appends them to the end of the players deck.
        """
        hand = self.get_hand()
        discarded = self.get_discarded()
        self._reset_cards()
        self._entity_attrs["cards"]["deck"].extend(hand + discarded)

    def end_turn(self) -> None:
        """Actions to take when a turn ends.

        Takes the cards in the players hand and appends them to the end of
        the discard pile.
        """
        hand = self.get_hand()
        self._reset_cards(0)
        self._entity_attrs["cards"]["discard pile"].extend(hand)

    def new_turn(self) -> None:
        """Actions to take when a new turn begins.

        Does the normal actions of the new_turn function from Entity as well
        as resetting player energy and drawing cards from the players deck.
        """
        super().new_turn()
        self._entity_attrs["energy"] = 3

        if len(self.get_deck()) == 0:
            self.get_deck().extend(self.get_discarded())
            self.get_discarded().clear()

        draw_cards(hand=self.get_hand(), deck=self.get_deck(),
                   discarded=self.get_discarded())

    def play_card(self, card_name: str) -> Card | None:
        """Searches through the players hand and plays the specified card if
        it's valid.

        Loops through the players hand, compares the cards name to card_name
        and then checks if the player's energy is great enough to play it.

        Parameters:
            card_name (str): The name of the card to play.
        """
        for card in self.get_hand():
            if (card.get_name() == card_name and
                    self.get_energy() >= card.get_energy_cost()):
                self._entity_attrs["cards"]["discard pile"].append(card)
                self._entity_attrs["cards"]["hand"].remove(card)
                self._entity_attrs["energy"] -= card.get_energy_cost()
                return card
        return None


class IronClad(Player):
    """Inherits from Player"""
    def __init__(self) -> None:
        """Initialises IronClad"""
        super().__init__(max_hp=80,
                         cards=([Strike()] * 5) + ([Defend()] * 4) + [Bash()]
                         )

    def __repr__(self) -> str:
        """Returns the string representation of an instance of this object"""
        return f"{self.__class__.__name__}()"


class Silent(Player):
    """Inherits from Player"""
    def __init__(self) -> None:
        """Initialises Silent"""
        super().__init__(max_hp=70,
                         cards=(([Strike()] * 5) + ([Defend()] * 5) +
                                [Neutralize(), Survivor()])
                         )

    def __repr__(self) -> str:
        """Returns the string representation of an instance of this object"""
        return f"{self.__class__.__name__}()"


class Monster(Entity):
    """Parent class to all Monster types, also a child to Entity.

    Sets up all methods for Monster classes and subclasses. All Monster's
    have access to MONSTER_ID.
    """

    MONSTER_ID = -1

    def __init__(self, max_hp: int) -> None:
        """Initialises the Monster class.

        Calls the __init__ method of the Entity class to set up basic
        functionality and implements extra methods for Monsters.

        Parameters:
             max_hp (int): The maximum (initial) hp of the monster.
        """
        super().__init__(max_hp=max_hp)
        Monster.MONSTER_ID += 1
        self._entity_attrs["uid"] = Monster.MONSTER_ID
        self._entity_attrs["action"] = NotImplementedError

    def get_id(self) -> int:
        """Returns the UID (Unique ID) of the monster."""
        return self._entity_attrs["uid"]

    def action(self) -> dict[str, int]:
        """Default, not implemented, monster action."""
        act = self._entity_attrs["action"]
        if act is not NotImplementedError:
            return act
        raise NotImplementedError


class Louse(Monster):
    """Subclass of Monster"""
    def __init__(self, max_hp: int) -> None:
        """Initialises an instance of Louse"""
        super().__init__(max_hp=max_hp)
        self._entity_attrs["action"] = {"damage": random_louse_amount()}
        if self.get_strength() > 0:
            self._entity_attrs["action"]["strength"] = self.get_strength()


class Cultist(Monster):
    """Subclass of Monster"""
    def __init__(self, max_hp: int) -> None:
        """Initialises an instance of Cultist"""
        super().__init__(max_hp=max_hp)
        self._entity_attrs["action calls"] = 0

    def action(self) -> dict[str, int]:
        """Returns a dictionary with the amount of damage, weak and strength
        applied."""
        calls = self._entity_attrs["action calls"]
        self._entity_attrs["action"] = {
            "damage": 0 if calls == 0 else 6 + calls,
            "weak": 0 if not bool(calls & 1) else 1}
        if self.get_strength() > 0:
            self._entity_attrs["action"]["strength"] = self.get_strength()
        self._entity_attrs["action calls"] += 1
        return self._entity_attrs["action"]


class JawWorm(Monster):
    """Subclass of Monster"""
    def __init__(self, max_hp: int) -> None:
        """Initialises an instance of JawWorm"""
        super().__init__(max_hp=max_hp)

    def action(self) -> dict[str, int]:
        """Returns a dictionary with the amount of damage, weak and strength
        applied."""
        self._entity_attrs["damage taken"] = (self._entity_attrs["max hp"] -
                                              self._entity_attrs["hp"])

        block_mod = 0
        if (block_mod := self._entity_attrs["damage taken"] / 2).is_integer():
            block_mod = int(block_mod)
        elif not block_mod.is_integer():
            block_mod = int(block_mod) + 1

        self.add_block(block_mod)
        self._entity_attrs["action"] = {
            "damage": int(self._entity_attrs["damage taken"] / 2)}
        if self.get_strength() > 0:
            self._entity_attrs["action"]["strength"] = self.get_strength()
        return self._entity_attrs["action"]


class Encounter:
    """Class to handle encounters.

    Sets up all methods for Encounter classes.
    """

    def __init__(self, player: Player, monsters: list[tuple[str, int]]) -> None:
        """Initialises  the Encounter class.

        Parameters:
            player (Player): The player.
            monsters (list[tuple[str, int]]): A list of the monsters in the
                encounter, [("Louse", 10), ("Cultist", 5), ...].

        Usage:
            >>> monsters = [("Louse", 15), ("Louse", 10)]
            >>> player = Silent()
            >>> encounter = Encounter(player, monsters)
        """
        self._encounter_attrs = {
            "player": player,
            "monsters": self._init_monsters(monsters),
            "player turn": True,
        }
        self._encounter_attrs["player"].start_new_encounter()
        self.start_new_turn()

    @staticmethod
    def _init_monsters(monsters: list[tuple[str, int]]) -> list[Monster]:
        """Turns the list into a list of monsters classes.

        Parameters:
            monsters (list[tuple[str, int]]): A list of the monsters in the
                encounter, [("Louse", 10), ("Cultist", 5), ...].
        """
        str_to_class = {monster_class.__name__.lower(): monster_class
                        for monster_class in Monster.__subclasses__()}
        active_monsters = [
            str_to_class[monster[0].lower()](monster[1])
            for monster in monsters
        ]
        return active_monsters

    def _get_monster_by_id(self,
                           monster_id: int) -> tuple[Monster, int] | \
                                               tuple[None, float]:
        """Finds and returns the monster and its index.

        Loops through the encounter's monsters, finds the monster
        corresponding to monster_id (if it exists) and returns the monster
        with its index in the encounters monster list. If it does not exist
        it returns (None, float("inf")).

        Parameters:
            monster_id (int): The id of the monster to find.

        Returns:
            Either (monster, index) or (None, float("inf"))
        """
        for index, monster in enumerate(self.get_monsters()):
            if monster_id == monster.get_id():
                return monster, index
        return None, float("inf")

    def _remove_by_id(self, monster_id: int) -> None:
        """Removes a monster from the monsters list.

        Loops through the monsters list and removes the monster corresponding
            to that id.

        Parameters:
            monster_id (int): The id of the monster to remove.
        """
        monster = self._get_monster_by_id(monster_id=monster_id)
        if monster[1] == float("inf"):
            return
        del self.get_monsters()[monster[1]]

    def _player_play_card(self, card_name: str,
                          target_id: int | None = None) -> Card | None:
        """Checks if the card the player is attempting to play is valid.

        Checks if the card is in the player's hand, the player has enough
        energy and (if the card needs it) the player has specified a target.

        Parameters:
            card_name (str): The name of the card.
            target_id (int | None): The ID of the monster being targeted
                (if any)

        Returns:
            The card or None, if it returns the card the move is valid,
            otherwise the player cannot make that move.
        """
        player = self.get_player()
        starting_player_energy = player.get_energy()
        starting_cards = (player.get_hand().copy(),
                          player.get_discarded().copy())
        card = self.get_player().play_card(card_name)

        if (
                (card is None) or
                (card.requires_target() and target_id is None) or
                (not self._encounter_attrs["player turn"])
        ):
            if card is not None:
                player.set_energy(starting_player_energy)
                player.set_cards(starting_cards[1], 2)
                player.set_cards(starting_cards[0], 1)
            return None
        return card

    def start_new_turn(self) -> None:
        """Starts a new player turn."""
        self._encounter_attrs["player"].new_turn()
        self._encounter_attrs["player turn"] = True

    def end_player_turn(self) -> None:
        """Ends the player's turn."""
        self._encounter_attrs["player"].end_turn()
        self._encounter_attrs["player turn"] = False
        for monster in self._encounter_attrs["monsters"]:
            monster.new_turn()

    def get_player(self) -> Player:
        """Gets the player object."""
        return self._encounter_attrs["player"]

    def get_monsters(self) -> list[Monster]:
        """Gets a list of Monsters still active in the encounter."""
        return self._encounter_attrs["monsters"]

    def is_active(self) -> bool:
        """Checks to see if any monsters are still alive (active)."""
        for monster in self.get_monsters():
            if not monster.is_defeated():
                return True
        return False

    def player_apply_card(self, card_name: str,
                          target_id: int | None = None) -> bool:
        """Plays the player's move

        Checks if the player can make the move, applies the effects of the card
        and the player's/monsters status mods and returns True if it worked and
        False if it did not.

        Parameters:
            card_name (str): The name of the card.
            target_id (int | None): The ID of what the player wants to
                target.

        Returns:
            True or False depending on if the move worked.
        """
        player = self.get_player()

        card = self._player_play_card(card_name=card_name, target_id=target_id)
        if card is None:
            return False

        # Check if required fields are filled, and it's the players turn

        monster = self._get_monster_by_id(monster_id=target_id)
        if monster[1] == float("inf") and target_id:
            return False

        player.add_block(card.get_block())
        if "strength" in card.get_status_modifiers():
            player.add_strength(card.get_status_modifiers()["strength"])

        if not card.requires_target():
            return True

        for effect in card.get_status_modifiers():
            if effect == "weak":
                monster[0].add_weak(
                    card.get_status_modifiers()["weak"])
            if effect == "vulnerable":
                monster[0].add_vulnerable(
                    card.get_status_modifiers()["vulnerable"])
        damage = int(card.get_damage_amount() +
                     player.get_strength() *
                     (1.5 if monster[0].get_vulnerable() > 0 else 1) *
                     (0.75 if player.get_weak() > 0 else 1))
        monster[0].reduce_hp(damage)
        if monster[0].is_defeated():
            self._remove_by_id(monster_id=target_id)
        return True

    def enemy_turn(self) -> None:
        """Plays the enemies turn.

        Applies all monster actions.
        """
        if self._encounter_attrs["player turn"]:
            return

        player = self.get_player()
        monsters = self.get_monsters()

        for monster in monsters:
            action = monster.action()
            action["damage"] += action.get("strength", 0)

            if "weak" in action:
                player.add_weak(action["weak"])
            if "vulnerable" in action:
                player.add_vulnerable(action["vulnerable"])

            damage = int(
                action["damage"] *
                (1.5 if monster.get_vulnerable() > 0 else 1) *
                (0.75 if player.get_weak() > 0 else 1)
            )
            player.reduce_hp(damage)
        self.start_new_turn()


def handle_move(
        move: str) -> tuple[int | float, None | tuple[str, int] | str]:
    """Handles user interaction.

    Parameters:
        move (str): The user's input.
    """
    mod_move = move.lower()
    if mod_move == "end turn":
        return 0, None
    elif mod_move.startswith("inspect "):
        if mod_move.endswith("deck"):
            return 1, None
        elif mod_move.endswith("discard"):
            return 2, None
    elif mod_move.startswith("describe "):
        return 3, move.split(" ", maxsplit=1)[1]
    elif mod_move.startswith("play "):
        if len(split_move := move.split(" ")) == 2:
            data = (split_move[-1].strip(),)
        elif len(split_move := move.split(" ")) == 3:
            data = (split_move[1].strip(), int(split_move[-1]))
        return 4, data
    return float("inf"), None


def main():
    # Implement this only once you've finished and tested ALL of the required
    player_classes = {player_class.__name__.lower(): player_class
                      for player_class in Player.__subclasses__()}
    cards = {card.__name__: card for card in Card.__subclasses__()}
    player = player_classes[input("Enter a player type: ").lower()]()
    monster_encounters = read_game_file(input("Enter a game file: "))

    for monster_encounter in monster_encounters:
        encounter = Encounter(player=player, monsters=monster_encounter)
        print("New encounter!\n")
        display_encounter(encounter)

        while True:
            if not encounter.is_active():
                print(ENCOUNTER_WIN_MESSAGE)
                encounter.end_player_turn()
                break

            move = handle_move(input("Enter a move: "))
            match move[0]:
                case 0:
                    encounter.end_player_turn()
                    encounter.enemy_turn()
                    if encounter.get_player().get_hp() <= 0:
                        print(GAME_LOSE_MESSAGE)
                        return
                    display_encounter(encounter)
                case 1:
                    print(f"\n{encounter.get_player().get_deck()}\n")
                case 2:
                    print(f"\n{encounter.get_player().get_discarded()}\n")
                case 3:
                    card_name = move[1]
                    print(f"\n{cards[card_name]().get_description()}\n")
                case 4:
                    play = encounter.player_apply_card(*move[1])
                    if play:
                        display_encounter(encounter)
                    else:
                        print(CARD_FAILURE_MESSAGE)
                case float("inf"):
                    print(f"\nInvalid command, {move=}\n")
    else:
        print(GAME_WIN_MESSAGE)


if __name__ == '__main__':
    main()
