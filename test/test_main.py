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

import select
from typing import Dict
from typing import List
from typing import NoReturn

from types import FunctionType, NoneType

from unittest import TestCase
from unittest import main as unittest_main

from unittest.mock import patch

from urllib.request import AbstractBasicAuthHandler

from genty import genty
from genty import genty_dataset

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


@genty
class TestMain(TestCase):

    @patch(target='sys.stdout', new_callable=StringIO)
    def test__list_help__list_all_functions_no_start__success(
            self, mock_stdout: StringIO
        ) -> NoReturn:

        false_value: bool = list_help(
            help_list=[function_one, function_two], start=False, help_item=0
        )

        expected_result: str = "TODO - Help Menu\n0 = Function One\n1 = Function Two\n"
        actual_result: str = mock_stdout.getvalue()

        self.assertFalse(false_value, "Did not return false as expected.")
        self.assertEqual(expected_result, actual_result, "Printed text was not as expected.")

    @patch(target="builtins.input", side_effect=deepcopy(SAMPLE_TITLE_DESCRIPTION))
    def test__add_item__adds_item_to_list__success(self, mock_input) -> NoReturn:

        expected_result: List[Dict[str, (str | bool | NoneType)]] = [
            deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)
        ]

        actual_result: List[Dict[str, (str | bool | NoneType)]] = add_item(todo_list=[])

        self.assertEqual(
            expected_result,
            actual_result,
            "Expected TODO list does not match actual TODO list."
        )

    @patch(target="src.main._get_item_number", return_value=0)
    @patch(target="src.main.remove_item", return_value=[])
    def test__add_item__toggles_completed_to_true__success(
            self,
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

        self.assertEqual(expected_result, actual_result, "Updated array was not as expected")

    @patch(target="src.main._get_item_number", return_value=0)
    def test__add_item__toggles_completed_to_false__success(
            self, mock__get_item_number: int
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

        self.assertEqual(expected_result, actual_result, "Updated array was not as expected")

    def test__add_item__item_to_edit_is_None_and_toggle_completed_is_true__raises_type_error(
            self,
        ) -> NoReturn:

        with self.assertRaises(TypeError) as type_error:
            add_item(
                todo_list=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)],
                toggle_completed=True
            )

        expected_value: str = ("Invalid passed parameter set."
            + "\nMust pass an item_to_edit if passing toggle_completed as true."
            + "\nitem_to_edit None"
            + "\ntoggle_completed True"
        )

        actual_value: str = type_error.exception.__str__()
        self.assertIn(expected_value, actual_value)

    @patch(target="builtins.input", side_effect=["Null", "1"])
    @patch(target='sys.stdout', new_callable=StringIO)
    def test___get_item_number__returns_an_item_number_after_failure_with_blank_prompt__success(
            self, mock_input, mock_stdout
        ) -> NoReturn:

        expected_return_value = 1
        actual_return_value = _get_item_number()

        self.assertIs(
            expected_return_value,
            actual_return_value,
            "_get_item_number() did not return 1"
        )

    @genty_dataset("remove", "edit", "toggle")
    @patch(target="builtins.input", side_effect=["Null", "1"])
    @patch(target='sys.stdout', new_callable=StringIO)
    def test___get_item_number__returns_an_item_number_after_failure_with_prompt__success(
            self, operation: str, mock_input: str, mock_stdout: str
        ) -> NoReturn:

        expected_return_value = 1
        actual_return_value = _get_item_number(operation=operation)

        self.assertIs(
            expected_return_value,
            actual_return_value,
            "_get_item_number() did not return 1"
        )

    @patch(target="src.main._get_item_number", return_value=0)
    def test__remove_item__removes_item_from_list_when_passed_no_item__success(
            self, mock__get_item_number: int
        ) -> NoReturn:

        expected_result: List[Dict[str, (str | bool | NoneType)]] = []

        actual_result: List[Dict[str, (str | bool | NoneType)]] = remove_item(
            todo_list=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)]
        )

        self.assertEqual(expected_result, actual_result, "Expected blank array was not blank.")

    def test__remove_item__removes_specified_item_from_list__success(self) -> NoReturn:

        expected_result: List[Dict[str, (str | bool | NoneType)]] = []

        actual_result: List[Dict[str, (str | bool | NoneType)]] = remove_item(
            [deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)], item_to_remove=0
        )

        self.assertEqual(expected_result, actual_result, "Expected blank array was not blank.")

    def test__remove_item__removes_last_item_from_list_correctly__success(self) -> NoReturn:

        expected_result: List[Dict[str, (str | bool | NoneType)]] = [
            deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM) for i in range(1, 5)
        ]

        expected_result.remove(deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM))

        self.assertEqual(
            expected_result,
            remove_item(
                [deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM) for i in range(1, 5)],
                item_to_remove=1
            ),
            "Expected blank array was not blank."
        )

    @patch(target="src.main.add_item", return_value=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)])
    @patch(target="src.main._get_item_number", return_value=0)
    @patch(target="src.main.remove_item", return_value=[])
    def test__edit_item__edits_item_i_in_list__success(
            self,
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

        self.assertEqual(expected_result, actual_result, "Updated array was not as expected")

    @patch(target="src.main.add_item", return_value=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)])
    @patch(target="src.main._get_item_number", return_value=0)
    @patch(target="src.main.remove_item", return_value=[])
    def test__edit_item__toggles_completed_to_true__success(
            self,
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

        self.assertEqual(expected_result, actual_result, "Updated array was not as expected")

    @patch(target="src.main.add_item", return_value=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)])
    @patch(target="src.main._get_item_number", return_value=0)
    @patch(target="src.main.remove_item", return_value=[])
    def test__edit_item__toggles_completed_to_false__success(
            self,
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

        self.assertEqual(expected_result, actual_result, "Updated array was not as expected")

    @patch(target="src.main.edit_item", return_value=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)])
    def test__checkoff_item__makes_item_completed__success(
            self, mock_edit_item: List[Dict[str, (str | bool | NoneType)]]
        ) -> NoReturn:

        expected_result: List[Dict[str, (str | bool | NoneType)]] = [
            deepcopy(SAMPLE_COMPLETED_LIST_ITEM)
        ]

        actual_result: List[Dict[str, (str | bool | NoneType)]] = checkoff_item(
            todo_list=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)]
        )

        self.assertEqual(expected_result, actual_result, "Did not check off item.")

    @patch(target="src.main.edit_item", return_value=[deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)])
    def test__uncheck_item__makes_item_as_not_completed__success(
            self, mock_edit_item: List[Dict[str, (str | bool | NoneType)]]
        ) -> NoReturn:

        expected_result: List[Dict[str, (str | bool | NoneType)]] = [
            deepcopy(SAMPLE_UNCOMPLETED_LIST_ITEM)
        ]

        actual_result: List[Dict[str, (str | bool | NoneType)]] = uncheck_item(
            todo_list=[deepcopy(SAMPLE_COMPLETED_LIST_ITEM)]
        )

        self.assertEqual(expected_result, actual_result, "Did not uncheck item.")

    @patch(target='sys.stdout', new_callable=StringIO)
    def test__render_todo_list__renders_todo_list__success(self, mock_stdout: StringIO) -> NoReturn:

        false_value: NoneType = render_todo_list(todo_list=[SAMPLE_UNCOMPLETED_LIST_ITEM])

        expected_result: str = (
            '"[\\n    {\\n        \\"title\\": \\"Sample Title\\",\\n        \\"description\\":'
            + ' \\"Sample Description\\",\\n        \\"completed\\": false\\n    }\\n]\\n"'
        )

        actual_result: str = str(dumps(mock_stdout.getvalue(), indent=4))

        self.assertFalse(false_value, "Did not return false as expected.")
        self.assertEqual(expected_result, actual_result, "Printed text was not as expected.")


if __name__ == '__main__':
    unittest_main()
