"""
Unit tests for the TODO List.

NOTE: Assertions are always in the format of:
 - Expected Result
 - Actual Result
 - Assertion Message

Licenced under the GNU Affero General Public License V3.0
https://www.gnu.org/licenses/agpl-3.0.en.html

TO THE GREATEST EXTENT PERMITTED BY LAW, THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR
ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from copy import deepcopy

from io import StringIO

from json import dumps


from typing import Dict
from typing import List
from typing import NoReturn

from types import FunctionType
from types import NoneType

from unittest.mock import MagicMock, patch

from pytest import ExceptionInfo, mark
from pytest import raises

from src.main import list_help
from src.main import add_item
from src.main import edit_item
from src.main import remove_item
from src.main import checkoff_item
from src.main import uncheck_item
from src.main import render_todo_list
from src.main import exit_the_program
from src.main import main as main_function
from src.main import _get_item_number


SAMPLE_UNCOMPLETED_LIST_ITEM: Dict[str, (str | bool)] = {
    "title": "Sample Title",
    "description": "Sample Description",
    "completed": False
}

SAMPLE_COMPLETED_LIST_ITEM: Dict[str, (str | bool)] = {
    "title": "Sample Title",
    "description": "Sample Description",
    "completed": True
}

SAMPLE_TITLE_DESCRIPTION: List = ["Sample Title", "Sample Description"]


def function_one() -> NoReturn:
    pass


def function_two() -> NoReturn:
    pass


FUNCTIONS_LIST: FunctionType = (function_one, function_two)


@patch(target='sys.stdout', new_callable=StringIO)
def test__list_help__list_all_functions_no_start__success(
        mock_stdout: StringIO
    ) -> NoReturn:

    false_value: bool = list_help(
        help_list=FUNCTIONS_LIST, start=False, help_item=0
    )

    expected_result: str = "TODO - Help Menu\n0 = Function One\n1 = Function Two\n"
    actual_result: str = mock_stdout.getvalue()

    assert false_value is False, "Did not return false as expected."
    assert expected_result == actual_result, "Printed text was not as expected."


@patch(target="builtins.input", side_effect=deepcopy(SAMPLE_TITLE_DESCRIPTION))
def test__add_item__adds_item_to_list__success(mock_input) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = add_item(todo_list=[])

    assert expected_result == actual_result, "Expected TODO list does not match actual TODO list."


@patch(target="src.main._get_item_number", return_value=0)
@patch(target="src.main.remove_item", return_value=[])
def test__add_item__toggles_completed_to_true__success(
        mock__get_item_number: int,
        mock_remove_item: List[Dict[str, (str | bool | NoneType)]]
    ) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM),
        deepcopy(SAMPLE_COMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = add_item(
        todo_list=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)],
        item_to_edit=0,
        toggle_completed=True
    )

    assert expected_result == actual_result, "Updated array was not as expected"


@patch(target="src.main._get_item_number", return_value=0)
def test__add_item__toggles_completed_to_false__success(
        mock__get_item_number: int
    ) -> NoReturn:

    expected_result:  List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_COMPLETED_LIST_ITEM),
        deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = add_item(
        todo_list=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)],
        item_to_edit=0,
        toggle_completed=True
    )

    assert expected_result == actual_result, "Updated array was not as expected"


def test__add_item__item_to_edit_is_None_and_toggle_completed_is_true__raises_type_error(
    ) -> NoReturn:

    with raises(ValueError) as value_error:
        add_item(
            todo_list=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)],
            toggle_completed=True
        )

    expected_value: str = ("Invalid passed parameter set."
        + "\nMust pass an item_to_edit if passing toggle_completed as true."
        + "\nitem_to_edit None"
        + "\ntoggle_completed True"
    )

    actual_value: str = value_error.value.__str__()
    assert expected_value == actual_value, "Expected error message not in error output."


@patch(target="builtins.input", side_effect=["Null", "1"])
@patch(target='sys.stdout', new_callable=StringIO)
def test___get_item_number__returns_an_item_number_after_failure_with_blank_prompt__success(
        mock_input, mock_stdout
    ) -> NoReturn:

    expected_return_value = 1
    actual_return_value = _get_item_number()

    assert expected_return_value is actual_return_value, "_get_item_number() did not return 1"


@mark.parametrize("operation", ("remove", "edit", "toggle"))
@patch(target="builtins.input", side_effect=["Null", "1"])
@patch(target='sys.stdout', new_callable=StringIO)
def test___get_item_number__returns_an_item_number_after_failure_with_prompt__success(
        mock_input: str, mock_stdout: str, operation: str
    ) -> NoReturn:

    expected_return_value = 1
    actual_return_value = _get_item_number(operation=operation)

    assert expected_return_value is actual_return_value, "_get_item_number() did not return 1"


@patch(target="src.main._get_item_number", return_value=0)
def test__remove_item__removes_item_from_list_when_passed_no_item__success(
        mock__get_item_number: int
    ) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = []

    actual_result: List[Dict[str, (str | bool | NoneType)]] = remove_item(
        todo_list=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)]
    )

    assert expected_result == actual_result, "Expected blank array was not blank."


def test__remove_item__removes_specified_item_from_list__success() -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = []

    actual_result: List[Dict[str, (str | bool | NoneType)]] = remove_item(
        [deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)], item_to_remove=0
    )

    assert expected_result == actual_result, "Expected blank array was not blank."


def test__remove_item__removes_last_item_from_list_correctly__success() -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM) for i in range(1, 5)
    ]

    expected_result.remove(deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM))
    
    actual_result: List[Dict[str, (str | bool | NoneType)]] = remove_item(
        [deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM) for i in range(1, 5)], item_to_remove=1
    )

    assert expected_result == actual_result, "Expected blank array was not blank."


@patch(target="src.main.add_item", return_value=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)])
@patch(target="src.main._get_item_number", return_value=0)
@patch(target="src.main.remove_item", return_value=[])
def test__edit_item__edits_item_i_in_list__success(
        mock__get_title_description: str,
        mock__get_item_number: int,
        mock_remove_item: List[Dict[str, (str | bool | NoneType)]]
    ) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = edit_item(
        todo_list=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)]
    )

    assert expected_result == actual_result, "Updated array was not as expected"


@patch(target="src.main.add_item", return_value=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)])
@patch(target="src.main._get_item_number", return_value=0)
@patch(target="src.main.remove_item", return_value=[])
def test__edit_item__toggles_completed_to_true__success(
        mock__add_item:List[Dict[str, (str | bool | NoneType)]],
        mock__get_item_number: int,
        mock_remove_item: List[Dict[str, (str | bool | NoneType)]]
    ) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_COMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = edit_item(
        todo_list=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)], toggle_completed=True
    )

    assert expected_result == actual_result, "Updated array was not as expected"


@patch(target="src.main.add_item", return_value=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)])
@patch(target="src.main._get_item_number", return_value=0)
@patch(target="src.main.remove_item", return_value=[])
def test__edit_item__toggles_completed_to_false__success(
        mock__add_item:List[Dict[str, (str | bool | NoneType)]],
        mock__get_item_number: int,
        mock_remove_item: List[Dict[str, (str | bool | NoneType)]],
    ) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = edit_item(
        todo_list=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)], toggle_completed=True
    )

    assert expected_result == actual_result, "Updated array was not as expected"


@patch(target="src.main.edit_item", return_value=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)])
def test__checkoff_item__makes_item_completed__success(
        mock_edit_item: List[Dict[str, (str | bool | NoneType)]]
    ) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_COMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = checkoff_item(
        todo_list=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)]
    )

    assert expected_result == actual_result, "Did not check off item."


@patch(target="src.main.edit_item", return_value=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)])
def test__uncheck_item__makes_item_as_not_completed__success(
        mock_edit_item: List[Dict[str, (str | bool | NoneType)]]
    ) -> NoReturn:

    expected_result: List[Dict[str, (str | bool | NoneType)]] = [
        deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)
    ]

    actual_result: List[Dict[str, (str | bool | NoneType)]] = uncheck_item(
        todo_list=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)]
    )

    assert expected_result == actual_result, "Did not uncheck item."


@patch(target='sys.stdout', new_callable=StringIO)
def test__render_todo_list__renders_todo_list__success(mock_stdout: StringIO) -> NoReturn:

    false_value: NoneType = render_todo_list(todo_list=[SAMPLE_UNCOMPLETED_LIST_ITEM])

    expected_result: str = (
        '"[\\n    {\\n        \\"title\\": \\"Sample Title\\",\\n        \\"description\\":'
        + ' \\"Sample Description\\",\\n        \\"completed\\": false\\n    }\\n]\\n"'
    )

    actual_result: str = str(dumps(mock_stdout.getvalue(), indent=4))

    assert false_value is False, "Did not return false as expected."
    assert expected_result == actual_result, "Printed text was not as expected."


# @mark.parametrize("functions_to_be_called, parameters", [
#     (list_help, exit_the_program), (add_item, exit_the_program),
#     (remove_item, exit_the_program), (edit_item, exit_the_program),
#     (checkoff_item, exit_the_program), (uncheck_item, exit_the_program),
#     (render_todo_list, exit_the_program), (exit_the_program)
# ])
# @patch(target="src.main._get_item_number")
# def test__main__calls_function_correctly_and_prints_start__success(
#         mock__get_item_number: MagicMock,
#         functions_to_be_called: List[FunctionType],
#         sample_functions: List[FunctionType]
#     ) -> NoReturn:

#     functions_list_array: List[int] = iter(lambda this_function: (
#         FUNCTIONS_LIST.index(this_function) for this_function in functions_to_be_called
#     ))

#     local_functions_list: List[FunctionType] = deepcopy(FUNCTIONS_LIST)
#     del local_functions_list[0]

#     with patch(target=f"{functions_to_be_called[0]}") as mock_function_to_call:

#         if functions_to_be_called[0] == list_help:

#             mock__get_item_number.return_value = functions_list_array
#             mock_function_to_call.return_value = False

#             expected_result: int = 0
#             actual_result: int = main_function(start=True, todo_list=[])

#             functions_to_be_called[0].assert_called_once_with(sample_functions)

#         elif functions_to_be_called[0] in local_functions_list:

#             mock__get_item_number.return_value = functions_list_array
#             mock_function_to_call.return_value = [deepcopy()]

#             expected_result: int = 0
#             actual_result: int = main_function(start=True, todo_list=[])

#             functions_to_be_called[0].assert_called_once_with()

#         assert expected_result == actual_result, "Main did not return 0."
