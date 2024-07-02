"""
CSSE1001 Assignment 1
Semester 1, 2023
"""

# Fill these in with your details
__author__ = "Alexander Burow"
__email__ = "Your Email"
__date__ = "03/07/2024"

from constants import *

RECIPE_NAME_PROMPT = "Please enter the recipe name: "
INGREDIENT_PROMPT = "Please enter an ingredient: "
CMD_PROMPT = "Please enter a command: "
EMPTY_MEAL_PLAN = "No recipe in meal plan yet."
RECIPE_NOT_EXIST = ("Recipe does not exist in the cook book.\n"
                    "Use the mkrec command to create a new recipe.")

QUIT = "q"
HELP = "h"
GENERATE = "g"
LIST = "ls"
LIST_RECIPE = "ls -a"
LIST_SHOPPING = "ls -s"
MAKE_RECIPE = "mkrec"
COMMANDS = [QUIT, HELP, GENERATE, LIST, LIST_RECIPE, LIST_SHOPPING, MAKE_RECIPE]


# Write your functions here
def get_recipe_name(recipe: tuple[str, str]) -> str:
    """:param recipe: The recipe we want the name of.
    :return: The name of the recipe.
    """
    return recipe[0]


def parse_ingredient(raw_ingredient_detail: str) -> tuple[float, str, str]:
    """
    :param raw_ingredient_detail: The ingredient details we want to parse.
    :return: The parsed ingredient details.
    """
    return (
        float(
            (ingrs := tuple(
                raw_ingredient_detail.split(" ", maxsplit=2)
            ))[0]),) + ingrs[1:]


def create_recipe() -> tuple[str, str]:
    """Prompts the user to create a recipe.
    :return: Returns the recipe name and it's ingredients as a tuple.
    """
    return (
        input(RECIPE_NAME_PROMPT),
        ",".join(ingr for ingr in iter(lambda: input(INGREDIENT_PROMPT), ""))
    )


def recipe_ingredients(
        recipe: tuple[str, str]) -> tuple[tuple[float, str, str]]:
    return tuple(parse_ingredient(ingr) for ingr in recipe[1].split(","))


def add_recipe(new_recipe: tuple[str, str],
               recipes: list[tuple[str, str]]) -> None:
    recipes.append(new_recipe)


def find_recipe(recipe_name: str,
                recipes: list[tuple[str, str]]) -> tuple[str, str] | None:
    return f[0] if (f := list(filter(lambda x: x[0] == recipe_name,
                                     recipes))) else None


def remove_recipe(name: str, recipes: list[tuple[str, str]]) -> None:
    (recipes.remove(rec)
     if ((rec := find_recipe(name, recipes)) is not None and rec in recipes)
     else None)


def get_ingredient_amount(ingredient: str,
                          recipe: tuple[str, str]) -> tuple[float, str] | None:
    return f[0] if (f := list(filter(
        lambda x: x[-1] == ingredient, recipe_ingredients(recipe)))) else None


def add_to_shopping_list(ingredient_details: tuple[float, str, str],
                         shopping_list: list[tuple[float, str, str] | None]
                         ) -> None:
    ((name := ingredient_details[2], amount := ingredient_details[0]),
     (ass := lambda array, value, pos: (
         array.pop(pos), array.insert(pos, value))),
     guard := False,
     [
         ass(shopping_list, (s_amount + amount, unit, name), i)
         for i, (s_amount, unit, s_name) in enumerate(shopping_list)
         if s_name == name and (guard := True)],
     (shopping_list.append(ingredient_details) if not guard else None)
     )


def remove_from_shopping_list(ingredient_name: str, amount: float,
                              shopping_list: list) -> None:
    (
        (ass := lambda array, value, pos: (
            array.pop(pos), array.insert(pos, value))),
        [
            ass(shopping_list, (n_amount, unit, s_name), i)
            if ((name_match := (s_name == ingredient_name)) and
                (n_amount := s_amount - amount) > 0) else (
                shopping_list.pop(i) if name_match and n_amount <= 0 else
                None
            )
            for i, (s_amount, unit, s_name) in enumerate(shopping_list)
        ]
    )


def generate_shopping_list(
        recipes: list[tuple[str, str]]) -> list[tuple[float, str, str]]:
    return (shop_list := [],
            [add_to_shopping_list(ingredient, shop_list)
             for recipe in recipes
             for ingredient in recipe_ingredients(recipe)])[0]


def display_ingredients(shopping_list: list[tuple[float, str, str]]) -> None:
    (
        pad_amounts := [0, 0, 0],
        justs := [">", "^", "<"],
        (update_amount :=
         lambda amount, i: (pad_amounts.pop(i), pad_amounts.insert(i, amount))
         if amount > pad_amounts[i] else None),
        [update_amount(len(str(detail)), i)
         for details in shopping_list
         for i, detail in enumerate(details)],
        [print(f"| {detail:{justs[i]}{pad_amounts[i] + (1 if i else 0)}} ",
               end="")
         if i < len(details) - 1 else
         print(f"| {detail:{justs[i]}{pad_amounts[i] + (1 if i else 0)}} |")
         for details in shopping_list
         for i, detail, in enumerate(details)]
    )


def sanitise_command(command: str) -> str:
    return (
        (trans := lambda s: s.translate(str.maketrans("", "", "01234567890"))),
        trans(command.lower()).strip())[-1]


def process_command(command: str) -> tuple[int, int | None, str | None]:
    return (g := (
        command := ((sanitise_command(com[0]), float(com[1]))
                    if (com := command.rsplit(" ", maxsplit=1)
                        )[-1].isdecimal()
                    else (sanitise_command(command), None)),

        ret_code := [0],
        name := [None],

        [(ret_code.pop(0), ret_code.append(p_ret_code))
         for p_ret_code, com in enumerate(COMMANDS)
         if command[0] == com],

        ((ret_code.pop(0), ret_code.append(len(COMMANDS)),
          name.append(command[0].split(" ", maxsplit=1)[1]))
         if command[0].startswith("add") else None),

        ((ret_code.pop(0), ret_code.append(len(COMMANDS) + 1),
          name.append(command[0].rsplit(" ", maxsplit=1)[-1]))
         if command[0].startswith("rm -i") and command[1] is not None
         else ((ret_code.pop(0), ret_code.append(len(COMMANDS) + 2),
                name.append(command[0].split(" ", maxsplit=1)[-1]))
               if command[0].startswith("rm") and command[1] is None else
               None))
    ), g[1][0], g[0][1], g[2][-1])[-3:]


def main():
    """ Write your docstring """
    # cook book
    # Write the rest of your code here
    (
        recipe_collection := [CHOCOLATE_PEANUT_BUTTER_SHAKE, BROWNIE, SEITAN,
                              CINNAMON_ROLLS, PEANUT_BUTTER,
                              MUNG_BEAN_OMELETTE],
        meal_plan := [],
        shop_list := [],
        execute_map := {1: lambda _: print(HELP_TEXT),
                        2: lambda _: (display_ingredients(
                            ([shop_list.append(item) for item in
                              generate_shopping_list(meal_plan)],
                             shop_list)[-1])
                                      if meal_plan else None),
                        3: lambda _: (print(meal_plan) if meal_plan else
                                      print(EMPTY_MEAL_PLAN)),
                        4: lambda _: print("\n".join(
                            get_recipe_name(recipe) for recipe in
                            recipe_collection)),
                        5: lambda _: (
                            display_ingredients(shop_list)
                            if shop_list else None),
                        6: lambda _: add_recipe(create_recipe(),
                                                recipe_collection),
                        7: lambda meta:
                        (add_recipe(details, meal_plan)
                         if (details := find_recipe(meta[2],
                                                    recipe_collection)) else
                         print(RECIPE_NOT_EXIST)),
                        8: lambda meta: remove_from_shopping_list(meta[2],
                                                               meta[1],
                                                               shop_list),
                        9: lambda meta: remove_recipe(meta[2], meal_plan)},
        execute := lambda x: execute_map[x[0]](x),
        [
            execute(process_command(command))
            for command in iter(lambda: input(CMD_PROMPT).lower(), "q")])


if __name__ == "__main__":
    main()
