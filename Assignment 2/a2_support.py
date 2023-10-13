import random

random.seed(10012023)

ENCOUNTER_WIN_MESSAGE = '\nYou have won the encounter!\n'
GAME_WIN_MESSAGE = '\nYou have won the game!\n'
GAME_LOSE_MESSAGE = '\nYou have lost the game!\n'
CARD_FAILURE_MESSAGE = '\nCard application failed.\n'


def display_encounter(encounter: 'Encounter') -> None:
    """ Displays the current state of an encounter is a user friendly format.
    
        Parameters:
            encounter (Encounter): The encounter to display.
    """
    print('MONSTERS')
    for monster in encounter.get_monsters():
        border = len(str(monster)) * '-'
        print(f'{border}\nMonster {monster.get_id()}\n{monster}\n{border}')
    print('\n\n')
    print('PLAYER')
    player = encounter.get_player()
    border = len(f'Hand: {str(player.get_hand())}') * '-'
    print(
        f'{border}\n{player.get_name()}\nHP: {player.get_hp()}/'
        f'{player.get_max_hp()}\nEnergy: {player.get_energy()}\n'
        f'Hand: {player.get_hand()}\nBlock: {player.get_block()} '
        f'Strength: {player.get_strength()} '
        f'Vulnerable: {player.get_vulnerable()} '
        f'Weak: {player.get_weak()}\n{border}'
    )


def read_game_file(filename: str) -> list[list[tuple[str, int]]]:
    """ Reads a game file and returns a list of information about the monsters
        in each encounter. The elements of this list are lists of tuples, where
        each tuple describes one monster in that encounter (in the format
        (monster_type, start_hp)).
    
        Parameters:
            filename (str): The name of the file to read.
        
        Returns:
            list[list[tuple[str, int]]]: A list of information about the
                                         monsters in each encounter (in order).
    """
    encounters = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('Encounter'):
                encounters.append([])
            elif line.strip() != '':
                monster_type, start_hp = line.strip().split(' ')
                encounters[-1].append((monster_type, int(start_hp)))

    return encounters


def select_cards(cards: list, amount: int) -> list['Card']:
    """ Selects an amount of cards from the cards list, removes those cards from
        the original cards list, and returns the selected cards.
    
        Parameters:
            cards (list): The list of cards to select from.
            amount (int): The amount of cards to select.
        
        Returns:
            list[Card]: The selected cards.
    """
    selected_indices = random.sample(range(len(cards)), k=amount)
    selected_cards = [cards[i] for i in selected_indices]
    for i in sorted(selected_indices, reverse=True):
        cards.pop(i)
    return selected_cards


def draw_cards(
        deck: list['Card'],
        hand: list['Card'],
        discarded: list['Card']
) -> None:
    """ Handles drawing cards from the deck to the hand at the beginning of a
        turn.
    
        Parameters:
            deck (list[Card]): The deck to draw from.
            hand (list[Card]): The hand to draw into.
            discarded (list[Card]): The discard pile used to replenish
                                    the deck if there aren't enough cards
                                    available.
    """
    hand.clear()
    if len(deck) < 5:
        hand.extend(deck)
        deck.clear()
        deck.extend(discarded)
        discarded.clear()
    hand.extend(select_cards(deck, 5 - len(hand)))


def random_louse_amount() -> int:
    """ (int) Returns a random amount of damage for a louse to give. """
    return random.randint(5, 7)
