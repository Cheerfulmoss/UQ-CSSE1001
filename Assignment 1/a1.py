"""
CSSE1001 Assignment 1
Semester 1, 2023
"""

# Fill these in with your details
__author__ = "Alexander Burow"
__email__ = "s4809430@student.uq.edu.au"
__date__ = "03/03/2023"
__version__ = "23032023.2015"

from constants import *


# Write your functions here
def num_hours() -> float:
    """Returns the number of hours spent on the project.
    """
    hours = 14
    minutes = 0
    return float(hours + (minutes / 60))


def display_help() -> None:
    """Prints the HELP_TEXT constant from constants.py.

    Usage:
        >>> display_help()
    """
    print(HELP_TEXT)


def get_recipe_name(recipe: tuple[str, str]) -> str:
    """Returns the name of the recipe.

    Takes in a recipe of the form tuple[str, str] and returns the name of the
    recipe.

    Parameters:
        recipe (tuple[str, str]): A recipe where the first str in the tuple is
            the name of the recipe and the second string is the recipes
            ingredients.

    Return:
        The name of the recipe inputted.

    Usage:
        >>> get_recipe_name(
        ("cinnamon rolls", "480 ml almond milk,170 g Nuttelex"))
        "cinnamon rolls"
    """
    return recipe[0]


def parse_ingredient(raw_ingredient_detail: str) -> tuple[float, str, str]:
    """Splits the ingredient into its three components.

    Takes in a formatted string of an ingredient and turns it into a tuple of
    format tuple[float, str, str] where the float is the amount of the
    ingredient and the two strings are the units and the ingredient name.

    Parameters:
        raw_ingredient_detail (str): The raw ingredient details from the user.

    Return:
        A tuple of the form tuple[float, str, str] where the float is the
        amount of the ingredient, and the two strings are the units and the
        ingredient name, in that order.

    Usage:
        >>> parse_ingredient("0.5 tsp coffee granules")
        (0.5, "tsp", "granules")
    """
    measurement, unit, ingredient = raw_ingredient_detail.split(" ", maxsplit=2)
    return float(measurement), unit, ingredient


def recipe_ingredients(recipe: tuple[str, str]) -> tuple[
    tuple[float, str, str]]:
    """Splits the recipe into its ingredients.

    Takes in a recipe of the form tuple[str, str] and splits the ingredients
    of the recipe into individual elements where each element if of the form
    tuple[float, str, str].

    Parameters:
        recipe (tuple[str, str]): The recipe that is to be processed, must be
            in the order (recipe_name, recipe_ingredients) with both being
            strings.

    Returns:
        The ingredients as a tuple of tuples, where each tuple within the
        tuple has the amount of that ingredient (the float) and the units and
        name of the ingredient, in that order.

    Usage:
        >>> recipe_ingredients(
        ("peanut butter", "300 g peanuts,0.5 tsp salt, 2 tsp oil"))
        ((300.0, "g", "peanuts"), (0.5, "tsp", "salt"), (2.0, "tsp", "oil"))
    """
    return tuple(parse_ingredient(raw_ingredient.strip()) for
                 raw_ingredient in recipe[1].split(","))


def add_recipe(new_recipe: tuple[str, str], recipes: list[tuple[str, str]]) -> \
        None:
    """Adds a recipe to the recipes list passed into the function.

    Parameters:
        new_recipe (tuple[str, str]): The recipe you want to add.
        recipes (list[tuple[str, str]]): The list of recipes you want to add
            it to.

    Usage:
        >>> recipes = []
        >>> recipe = ("peanut butter", "300 g peanuts,0.5 tsp salt,2 tsp oil")
        >>> add_recipe(recipe, recipes)
    """
    recipes.append(new_recipe)


def get_ingredient_amount(ingredient: str, recipe: tuple[str, str]) -> \
        tuple[float, str] | None:
    """Gets the specific ingredients measurements from the recipe.

    Loops through all the ingredients in the recipe and compares the name of
    each ingredient to the one inputted into the function. If it is found the
    amounts of the ingredient is returned, otherwise returns None.

    Parameters:
        ingredient (str): The name of the ingredient.
        recipe (tuple[str, str]): The recipe you want to get the ingredients
            measurements from.

    Returns:
        A tuple containing the amount of the ingredient and the units they"re
        in or None if the ingredients is not in the recipe.

    Usage:
        >>> recipe = ("peanut butter", "300 g peanuts,0.5 tsp salt,2 tsp oil")
        >>> get_ingredient_amount("peanuts", recipe)
        (300, "g")
    """
    ingredients = recipe_ingredients(recipe)
    for recipe_ingredient in ingredients:
        if recipe_ingredient[2].lower() == ingredient.lower():  # Compares
            # ingredient names
            return recipe_ingredient[:2]


def remove_recipe(name: str, recipes: list[tuple[str, str]]) -> None:
    """Removes the first occurrence of the specified recipe from recipes.

    Uses find_recipe to check if the recipe is in recipes, if so it is
    removed from the list, otherwise it does nothing.

    Parameters:
        name (str): The name of the recipe.
        recipes (list[tuple[str, str]]): The list of recipes.

    Usage:
        >>> recipes = [
        ("peanut butter", "300 g peanuts,0.5 tsp salt,2 tsp oil")]
        >>> remove_recipe("peanut butter", recipes)
    """
    if (recipe := find_recipe(recipe_name=name, recipes=recipes)) is not None:
        recipes.remove(recipe)


def find_recipe(recipe_name: str, recipes: list[tuple[str, str]]) -> \
        tuple[str, str] | None:
    """Tries to find the given recipe within recipes.

    Loops through recipes, if the recipe name is found the recipe is
    returned, otherwise returns None.

    Parameters:
        recipe_name (str): The name of the recipe you want to find.
        recipes (list[tuple[str, str]]): The list of recipes you want to look
            through.

    Returns:
        Either returns None or if the recipe is found it returns the recipe.

    Usage:
        >>> recipes = [
        ("peanut butter", "300 g peanuts,0.5 tsp salt,2 tsp oil")]
        >>> find_recipe("peanut butter", recipes)
        ("peanut butter", "300 g peanuts,0.5 tsp salt,2 tsp oil")
        >>> find_recipe("something not in the list")
        None
    """
    for recipe in recipes:
        if get_recipe_name(recipe).lower() == recipe_name.lower():
            return recipe


def create_recipe() -> tuple[str, str]:
    """A function to create recipes from user input.

    Prompts the user for a recipe name and then continually prompts the user
    for ingredients ( of the form 50 ml milk / amount units name ),
    this prompting stops when the user simply presses enter without typing
    anything. The recipe of the form ("recipe name", "ingredient_1,
    ingredient_2,...") is returned.

    Returns:
         A tuple containing the recipe name and the ingredients, both as
         strings.
    """
    ingredients = list()
    recipe_name = input("Please enter the recipe name: ")
    while True:
        raw_ingredient = input("Please enter an ingredient: ") + ","

        if raw_ingredient == ",":  # breaks if the user inputted nothing
            break

        ingredients.append(raw_ingredient)
    return recipe_name, "".join(ingredients)[:-1]  # returns [:-1] due to
    # trailing ","


def add_to_shopping_list(ingredient_details: tuple[float, str, str],
                         shopping_list: list[
                             tuple[float, str, str] | None]) -> None:
    """Adds the specified ingredient to the shopping list.

    Loops through shopping_list, first checks if the ingredients name is
    already in the list, if so the amounts ( already within the list and from
    ingredient_details ) are summed, otherwise the ingredient is appended
    onto the list as is.

    Parameters:
        ingredient_details (tuple[float, str, str]): A tuple containing the
            amount of the ingredient, the units and the name, in that order.
        shopping_list (list[tuple[float, str, str] | None]): The shopping
            list you want to add to.

    Usage:
        >>> shopping_list = [(300.0, "g", "peanuts"), (0.5, "tsp", "salt"),
        (2.0, "tsp", "oil")]
        >>> add_to_shopping_list((1000.0, "g", "tofu"), shopping_list)
        >>> shopping_list
        [(300.0, "g", "peanuts"), (0.5, "tsp", "salt"), (2.0, "tsp", "oil"),
        (1000.0, "g", "tofu")]
        >>> add_to_shopping_list((1200.0, "g", "peanuts"), shopping_list)
        >>> shopping_list
        [(1500.0, "g", "peanuts"), (0.5, "tsp", "salt"), (2.0, "tsp", "oil"),
        (1000.0, "g", "tofu")]
    """
    for ingredient in shopping_list:
        if ingredient[2].lower() == ingredient_details[2].lower():  # Compares
            # ingredient names
            amount = ingredient[0] + ingredient_details[0]
            shopping_list.remove(ingredient)
            break
    else:
        amount = ingredient_details[0]
    shopping_list.append((amount, *ingredient_details[1:]))


def remove_from_shopping_list(ingredient_name: str, amount: float,
                              shopping_list: list) -> None:
    """Removes the specified amount of ingredient from the shopping list.

    Loops through the shopping_list, if the ingredient is in the list the
    amount of that ingredient is decreased by the amount inputted into the
    function. The item is then removed from the shopping list, then the new
    amount is checked, if amount <= 0 the function does nothing and exits
    otherwise the recipe is appended with the new amount.

    Parameters:
        ingredient_name (str): The name of the ingredient you want to modify.
        amount (float): The amount to remove from the ingredient.
        shopping_list (list[tuple[float, str, str] | None]): The shopping
            list you want to add to.

    Usage:
        >>> shopping_list = [(0.5, "tsp", "salt"), (2.0, "tsp", "oil"),
        (1500.0, "g", "peanuts")]
        >>> remove_from_shopping_list("peanuts", 500, shopping_list)
        >>> shopping_list
        [(0.5, "tsp", "salt"), (2.0, "tsp", "oil"), (1000.0, "g", "peanuts")]
        >>> remove_from_shopping_list("peanuts", 1000, shopping_list)
        >>> shopping_list
        [(0.5, "tsp", "salt"), (2.0, "tsp", "oil")]
    """
    for ingredient in shopping_list:
        if ingredient[2].lower() == ingredient_name.lower():
            amount = ingredient[0] - amount
            shopping_list.remove(ingredient)
            if amount > 0:
                shopping_list.append((amount, *ingredient[1:]))
            return


def generate_shopping_list(recipes: list[tuple[str, str]]) -> list[tuple[
    float, str, str]]:
    """Makes a list of ingredients from a list of recipes.

    Loops through recipes and adds it into a dictionary where the keys of the
    dictionary are the ingredient names ( e.g. {"butter": <value>,
    "chocolate": <value>,...} ) and the values are also dictionaries
    ( {"amount": <float e.g. 0.25>, "units": <str e.g. "ml">} ).
    The dictionary is used as a simple way to handle duplicates. The
    dictionary is then pulled back apart into a list where each value is a
    tuple of the form (amount, units, name), e.g. [(300.0, "g", "peanuts"),
    (10.0, "ml", "water"),...].

    Parameters:
        recipes (list[tuple[str, str]]): The list of recipes you want a
            shopping list for.

    Returns:
        A list of ingredients of the form (amount, units, name).

    Usage:
        >>> shopping_list = generate_shopping_list([PEANUT_BUTTER,
        MUNG_BEAN_OMELETTE])
        >>> shopping_list
        [(300.0, "g", "peanuts"), (1.0, "tsp", "salt"), (3.0, "tsp", "oil"),
        (1.0, "cup", "mung bean"), (0.75, "tsp", "pink salt"),
        (0.25, "tsp", "garlic powder"), (0.25, "tsp", "onion powder"),
        (0.125, "tsp", "pepper"), (0.25, "tsp", "turmeric"),
        (1.0, "cup", "soy milk")]
    """
    # A dictionary is used to simplify the process of finding duplicates
    unique_shopping_list = dict()
    for recipe in recipes:
        # Loops through the ingredients
        for amount, units, name in recipe_ingredients(recipe):

            if name in unique_shopping_list:  # If already in dictionary
                unique_shopping_list[name]["amount"] += amount
                continue
            unique_shopping_list[name] = {"amount": amount, "units": units}

    # Turns the dictionary back into the list format
    return [
        (unique_shopping_list[key]["amount"],
         unique_shopping_list[key]["units"], key)
        for key in unique_shopping_list]


def display_ingredients(shopping_list: list[tuple[float, str, str]]) -> None:
    """Displays the ingredients of a shopping list as a table.

    Loops through shopping_list ( if it is populated, otherwise it exits )
    and adds it into a dictionary where the keys of the dictionary are the
    ingredient names ( e.g. {"butter": <value>, "chocolate": <value>,...} )
    and the values are also dictionaries ( {"amount": <float e.g. 0.25>,
    "units": <str e.g. "ml">} ). Next the maximum widths of each column is
    found ( the columns being amount, units, name ). Finaly the table is
    constructed using the maximum widths as padding, and then it is displayed
    to the user.

    Parameters:
        shopping_list (list[tuple[float, str, str]]): The shopping list with
            the ingredients you want displayed.

    Usage:
        >>> display_ingredients(
        [(1.0, "large", "banana"), (0.5, "cup", "ice"),])
        | 1.0 | large | banana |
        | 0.5 | cup   | ice    |
    """
    # Do nothing or the function errors out.
    if len(shopping_list) == 0:
        return

    # Turns the ingredients into a dictionary to make it easier to format the
    # table later, this does not need the same checking code as in
    # generate_shopping_list as this is run afterwards.
    ingredients = {name: {"amount": amount, "units": units}
                   for amount, units, name in shopping_list}

    # Constructs a list of word lengths per row, uses an iterator
    # with the zip command to reshape the list from from
    # [0, 1 ,2 ,3, 4, 5, ...] into form [(0, 1, 2), (3, 4, 5), ...].
    column_entry_widths = list(zip(column_entry_widths := (
        len(str(item)) if type(item) is float else len(item)
        for ingredient in shopping_list for item in ingredient),
                                   column_entry_widths, column_entry_widths))

    # unpacks and zips column_entry_widths into a different configuration.
    # From list of lengths per ingredient/row -> list of lengths per column.
    # Then the max of each list is grabbed which is the padding needed for each
    # column.
    max_lens = tuple(max(column_lengths) for column_lengths in
                     list(zip(*column_entry_widths)))

    table = list(
        (
            "| {amount: >{pad_a}} |"
            " {units: ^{pad_u}} |"
            " {ingredient: <{pad_i}} |".format(
                amount=str(ingredients[ingredient]["amount"]),
                pad_a=max_lens[0], units=str(ingredients[ingredient]["units"]),
                pad_u=max_lens[1] + 1, ingredient=ingredient,
                pad_i=max_lens[2] + 1
            )
        )
        for ingredient in sorted(ingredients, key=lambda wrd: wrd.upper())
    )
    print("\n".join(table))


def sanitise_command(command: str) -> str:
    """Returns a cleaned command string with numbers and whitespace removed.

    Loops through the characters in the command string, if the character is a
    digit it is skipped otherwise the character is appended to a list,
    the list is then joined back to a string and stripped of any
    leading/trailing whitespace.

    Parameters:
        command (str): The command to sanitise

    Usage:
        >>> command = sanitise_command("add chocolate brownies")
        >>> command
        "add chocolate brownies"
        >>> command = sanitise_command("add chocolate Brownies         5")
        >>> command
        "add chocolate brownies"
    """
    return ("".join("" if char.isdigit() else char for char in
                    command).strip().lower())


def process_command(command: str, condition: int) -> any:
    """Takes in a command collected from the user and processes/cleans it.

    Takes in a command string and condition, depending on the condition the
    command string is manipulated differently and then returned for further
    processing.

    Parameters:
        command (str): The command to process.
        condition (int): The case in which the command was collected,
            to determine what to do with the command. Condition can take on
            three states:
            condition = 0: Adding/removing a recipe to/from recipes.
            condition = 1: Removing or decreasing an ingredient from the
            shopping list.

    Returns:
        Anything depending on the command it is processing, these include;
    """
    command = command.lower()
    match condition:
        case 0:  # adding/removing recipes
            command = sanitise_command(command=command)
            recipe_name = command.split(" ", maxsplit=1)[1]
            return recipe_name
        case 1:  # removing items from the shopping list
            command = command.removeprefix("rm -i").strip()
            name, amount = command.rsplit(" ", maxsplit=1)
            return name.strip(), amount.strip()


def main():
    """Handles all high level user interactions.

    All top level commands are handled by this function and any sub-commands
    are handled by other functions. Also holds user info such as the cook
    book, recipes and shopping list.
    """
    # cook book
    cook_book = {
        CHOCOLATE_PEANUT_BUTTER_SHAKE[0]: CHOCOLATE_PEANUT_BUTTER_SHAKE[1],
        BROWNIE[0]: BROWNIE[1],
        SEITAN[0]: SEITAN[1],
        CINNAMON_ROLLS[0]: CINNAMON_ROLLS[1],
        PEANUT_BUTTER[0]: PEANUT_BUTTER[1],
        MUNG_BEAN_OMELETTE[0]: MUNG_BEAN_OMELETTE[1]
    }

    # Write the rest of your code here
    recipes = list()
    shopping_list = list()
    while True:
        user_input = input("Please enter a command: ")
        user_input = user_input.strip()
        sani_command = sanitise_command(user_input)

        if sani_command == "q":
            return

        elif sani_command == "h":
            display_help()

        elif sani_command.startswith("add "):
            recipe_name = process_command(command=user_input, condition=0)
            if recipe_name not in cook_book:
                print("\nRecipe does not exist in the cook book. ")
                print("Use the mkrec command to create a new recipe.\n")
                continue

            recipe = (recipe_name, cook_book[recipe_name])
            add_recipe(new_recipe=recipe, recipes=recipes)

        elif sani_command.startswith("rm -i"):
            name, amount = process_command(user_input, condition=1)
            remove_from_shopping_list(ingredient_name=name,
                                      amount=float(amount),
                                      shopping_list=shopping_list)

        elif sani_command.startswith("rm "):
            recipe_name = process_command(command=user_input, condition=0)
            remove_recipe(name=recipe_name,
                          recipes=recipes)

        elif sani_command == "g":
            shopping_list = generate_shopping_list(recipes=recipes)
            display_ingredients(shopping_list=shopping_list)

        elif sani_command == "ls":
            if len(recipes) == 0:
                print("No recipe in meal plan yet.")
            else:
                print(recipes)

        elif sani_command == "ls -a":
            for key in cook_book:
                print(key)

        elif sani_command == "ls -s":
            display_ingredients(shopping_list=shopping_list)

        elif sani_command == "mkrec":
            key, value = create_recipe()
            cook_book[key] = value


if __name__ == "__main__":
    main()
