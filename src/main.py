"""
Functional Python program to operate a TODO list. (Yes I deliberately wrote it that way.)

Licenced under the GNU Affero General Public License V3.0
https://www.gnu.org/licenses/agpl-3.0.en.html

TO THE GREATEST EXTENT PERMITTED BY LAW, THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR
ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

# First Party Imports
from copy import deepcopy

from inspect import signature
from inspect import getmembers

from json import dumps

from sys import exit as close_program
from sys import modules

from typing import Dict
from typing import List
from typing import NoReturn

from types import FunctionType
from types import NoneType

# Third Party Imports
from funcs import raises


def list_help(help_list: List[FunctionType], start: bool = False, help_item: int = 0) -> bool:
    """
    Print a list of functions as strings against the list position number for that item.

    This function takes in a list of functions and sequentially iterates over that list using
    recursion to print out each item in the list against the positional number in that list.

    The format for this is as follows:
        `Item Number (0, 1, 2, etc.) = Function Name (Add Item, Edit Item, etc.)`

    The list_item object is what dos the conversion process from, for example, `add_item` into
    'Add Item'. This is done by getting the current item's name and then splitting it on the
    underscore thus creating an iterable that can be mapped against to capitalise the first letter
    of. We then join that back up using the join function on ' ' to convert it into spaced words.

    :param help_list: The list of functions to be printed.
    :type help_list: List[FunctionType]

    :param start: Whether or not the function is being run for the first time.
    :type start: bool = False

    :param help_item: The current point we are at in the help_list.
    :type help_item: int = 0

    :returns: False when having recursed through the `help_list`.
    :rtype: bool
    """

    start = bool(print("Welcome to TODO. What would you like to do?") if start is True else False)
    help_item = int(bool(print("TODO - Help Menu"))) if help_item == 0 and not start else help_item

    # Here we convert the name of the function, say ``
    list_item = ' '.join(
        map(lambda word : word.capitalize(), (help_list[help_item].__name__).split(sep='_')
    ))

    print(f"{help_item} = {list_item}")

    return ( # The below code looks clearer with the brackets around help_item + 1.
        list_help(help_list=help_list, help_item=(help_item + 1)) # pylint: disable=superfluous-parens
        if help_item < (len(help_list) - 1)
        else False
    )


def add_item(
            todo_list: List[Dict[str, (str | bool | NoneType)]],
            item_to_edit: (int | NoneType) = None,
            toggle_completed: bool = False
        ) -> List[Dict[str, (str | bool | NoneType)]]:
    """
    Add an item to the TODO list.

    This function will add an item to the passed in TODO list and then return the updated TODO list.

    Items added to the TODO list default to incomplete.

    ---

    Execution Conditions based on parameters:
     - item_to_edit is integer and toggle_completed -> toggle specific item completed_status
     - item_to_edit is integer and not toggle_completed -> edit specific item
     - item_to_edit is None and toggle_completed -> error
     - item_to_edit is None and not toggle_completed -> add item to list

    ---

    :param todo_list: The TODO list to add an item to.
    :type todo_list: List[Dict[str, (str | bool | NoneType)]]

    :returns: The updated TODO list.
    :rtype: List[Dict[str, (str | bool | NoneType)]]
    """

    def _raise_type_error(message: str) -> NoReturn:
        raise TypeError(message)

    next_error: str = ("Invalid passed parameter set."
        + "\nMust pass an item_to_edit if passing toggle_completed as true."
        + f"\nitem_to_edit {item_to_edit}"
        + f"\ntoggle_completed {toggle_completed}"
    )

    completed_status: bool = (
        _raise_type_error(message=next_error)
        if item_to_edit is None and toggle_completed
        else (False if item_to_edit is None else todo_list[item_to_edit].get("completed", False))
    )

    # In the below case the code is not unreachable. This is a misunderstanding by PyLint.
    return deepcopy(todo_list) + [{ # pylint: disable=unreachable
        "title": (
            todo_list[item_to_edit].get("title", None)
            if toggle_completed
            else str(input("Enter a title for the item in question.\n>>> "))
        ),
        "description": (
            todo_list[item_to_edit].get("description", None)
            if toggle_completed
            else str(input("Enter a description for the item in question.\n>>> "))
        ),
        "completed": not bool(completed_status) if toggle_completed else completed_status
    }]


def _get_item_number(operation: str = "", retry: bool = False) -> int:
    """
    Get the item number of the TODO list item to be operated on.

    :param operation: The operation that's being performed that's requesting an item number.
    :type operation: str = ""

    :returns: The number of the selected item.
    :rtype: int
    """

    print("You may only enter digits.") if retry else False

    next_prompt: str = ("" if operation not in ["remove", "edit", "toggle"] else (
        f"Enter the number of the list item you want to {operation}."
    ))

    item_number: str = input(prompt=f"{next_prompt}\n>>> ")

    return (
        int(item_number)
        if item_number.isdigit()
        else _get_item_number(operation=operation, retry=True)
    )


def remove_item(
            todo_list: List[Dict[str, (str | bool | NoneType)]],
            item_to_remove: (int | NoneType) = None,
        ) -> List[Dict[str, (str | bool | NoneType)]]:
    """
    Remove an item from the TODO list.

    This function will ask the user which item they want to remove from the passed in TODO list,
    then update the TODO list and return the updated version.

    :param todo_list: The TODO list to remove an item from.
    :type todo_list: List[Dict[str, (str | bool | NoneType)]]

    :returns: The updated TODO list.
    :rtype: List[Dict[str, (str | bool | NoneType)]]
    """

    return_list: List[Dict[str, (str | bool | NoneType)]] = deepcopy(todo_list)

    this_item_to_remove: (int | NoneType) = (
        _get_item_number(operation="remove")
        if item_to_remove is None
        else item_to_remove
    )

    return return_list[:this_item_to_remove] + (
        return_list[(this_item_to_remove + 1):]
        if (this_item_to_remove + 1) < len(return_list)
        else []
    )


def edit_item(
            todo_list: List[Dict[str, (str | bool | NoneType)]],
            toggle_completed: bool = False
        ) -> List[Dict[str, (str | bool | NoneType)]]:
    """
    Edit an item in the TODO list.

    This function will ask the user which item they want to edit from the passed in TODO list,
    then update the TODO list and return the updated version.

    :param todo_list: The TODO list to edit an item in.
    :type todo_list: List[Dict[str, (str | bool | NoneType)]]

    :returns: The updated TODO list.
    :rtype: List[Dict[str, (str | bool | NoneType)]]
    """

    item_to_edit: int = _get_item_number(operation=("edit" if not toggle_completed else "toggle"))

    return add_item(
        todo_list=remove_item(todo_list=deepcopy(todo_list), item_to_remove=item_to_edit),
        item_to_edit=item_to_edit,
        toggle_completed=toggle_completed
    )


def checkoff_item(
            todo_list: List[Dict[str, (str | bool | NoneType)]]
        ) -> List[Dict[str, (str | bool | NoneType)]]:
    """
    Check off an item in the TODO list.

    This function will ask the user which item they want to check off in the passed in TODO list,
    then update the TODO list accordingly and return the updated version.

    :param todo_list: The TODO list to check off an item from.
    :type todo_list: List[Dict[str, (str | bool | NoneType)]]

    :returns: The updated TODO list.
    :rtype: List[Dict[str, (str | bool | NoneType)]]
    """
    return edit_item(todo_list=todo_list, toggle_completed=True)


def uncheck_item(
            todo_list: List[Dict[str, (str | bool | NoneType)]]
        ) -> List[Dict[str, (str | bool | NoneType)]]:
    """
    Uncheck an item in the TODO list.

    This function will ask the user which item they want to uncheck in the passed in TODO list,
    then update the TODO list accordingly and return the updated version.

    :param todo_list: The TODO list to check off an item from.
    :type todo_list: List[Dict[str, (str | bool | NoneType)]]

    :returns: The updated TODO list.
    :rtype: List[Dict[str, (str | bool | NoneType)]]
    """
    return edit_item(todo_list=todo_list, toggle_completed=True)


def render_todo_list(todo_list: List[Dict[str, (str | bool | NoneType)]]) -> NoneType:
    """
    Display the TODO list to the user.

    This function prints the TODO list to the console.

    :param todo_list: The TODO list to check off an item from.
    :type todo_list: List[Dict[str, (str | bool | NoneType)]]

    :returns: None
    :rtype: NoneType
    """
    return print(str(dumps(todo_list, indent=4)))


def exit_the_program() -> NoReturn:
    """
    Returns the condition required to close the program.

    :returns: A string with the text "Exit the program."
    :rtype: str = "Exit the program."
    """
    return "Exit the program."


def main(start: bool, todo_list: List[Dict[str, (str | bool | NoneType)]]) -> None:
    """
    Main function to allow the user to select which operation in the TODO list.

    `help_list` is generated by filtering down the list of functions in the module (retrieved using
    the `getmembers()` function - the iterable for this `filter()` operation) such that it removes
    any private functions.

    This is selected by checking if the function is a dunder (Python's equivalent of private
    functions operating on "a gentleman's agreement" to not call them outside of the declaring
    module) function or if the function is this main function. That's done by checking if the
    function stats with two underscores or if its name is "main".

    We then generate the iterable for the filter by calling the `getmembers()` function to get the
    members list. We use a predicate that limits what's collected to functions in the module so we
    don't end up collecting globals or the like.

    :param start: Whether or not the function is being run for PyMonadthe first time.
    :type start: bool = False

    :param todo_list: The TODO list to check off an item from.
    :type todo_list: List[Dict[str, (str | bool | NoneType)]]

    :returns: None
    :rtype: NoneType
    """

    help_list: List[FunctionType] = filter(
        lambda this_function: not(
            bool(this_function.__name__.startswith("__"))
            or bool(this_function.__name__.startswith("_"))
            or this_function.__name__ == "main"
        ),
        getmembers(
            object=modules[__name__],
            predicate=lambda this_object: (
                isinstance(this_object, FunctionType)
                and this_object.__module__ == __name__
            )
        )
    )

    render_todo_list(todo_list=todo_list)
    next_start: bool = list_help(help_list=help_list, start=start) if start is True else False
    selected_option: int = _get_item_number()

    return_value: (bool | List[Dict[str, (str | bool | NoneType)]]) = help_list[selected_option]( # pylint: disable=unsubscriptable-object
        *map( # pylint: disable=unsubscriptable-object
            func=lambda attribute : getattr(main, attribute),
            iterable=signature(obj=help_list[selected_option]).format() # pylint: disable=unsubscriptable-object
        )
    )

    return (0 if return_value == "Exit the program." else main(start=next_start, todo_list=(
        return_value if not isinstance(return_value, bool) else deepcopy(todo_list)
    )))


if __name__ == "__main__": # pragma: no cover
    close_program(main(start=True, todo_list=[]))
