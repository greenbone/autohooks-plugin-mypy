#!/usr/bin/env python3

# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from autohooks.api.git import StatusEntry
from autohooks.config import load_config_from_pyproject_toml

from autohooks.plugins.mypy.mypy import (
    DEFAULT_ARGUMENTS,
    DEFAULT_INCLUDE,
    check_mypy_installed,
    ensure_iterable,
    get_include_from_config,
    get_mypy_arguments,
    get_mypy_config,
    precommit,
)


def get_test_config_path(name):
    return Path(__file__).parent / name


class AutohooksMypyTestCase(TestCase):
    def test_mypy_installed(self):
        path = sys.path
        sys.path = []
        with self.assertRaises(Exception):
            check_mypy_installed()
        sys.path = path

    def test_get_mypy_arguments(self):
        args = get_mypy_arguments(config=None)
        self.assertEqual(args, DEFAULT_ARGUMENTS)

    def test_get_mypy_config(self):
        config_path = get_test_config_path("pyproject.test.toml")
        self.assertTrue(config_path.is_file())

        autohooksconfig = load_config_from_pyproject_toml(config_path)

        mypy_config = get_mypy_config(autohooksconfig.get_config())
        self.assertEqual(mypy_config.get_value("foo"), "bar")

    def test_ensure_iterable(self):
        foo = "bar"  # pylint: disable=disallowed-name
        bar = ensure_iterable(foo)  # pylint: disable=disallowed-name
        self.assertEqual(bar, ["bar"])

        foo = ["bar"]  # pylint: disable=disallowed-name
        bar = ensure_iterable(foo)  # pylint: disable=disallowed-name
        self.assertEqual(bar, ["bar"])

    def test_get_include_from_config(self):
        include = get_include_from_config(config=None)
        self.assertEqual(include, DEFAULT_INCLUDE)

    @patch("autohooks.plugins.mypy.mypy.ok")
    def test_precommit_no_files(self, _ok_mock):
        ret = precommit()
        self.assertFalse(ret)

    # these Terminal output functions don't run in the CI ...
    # @patch('sys.stdout', new_callable=StringIO)
    @patch("autohooks.plugins.mypy.mypy.ok")
    @patch("autohooks.plugins.mypy.mypy.out")
    @patch("autohooks.plugins.mypy.mypy.error")
    @patch("autohooks.plugins.mypy.mypy.get_staged_status")
    def test_precommit_errors(
        self,
        staged_mock,
        _error_mock,
        _out_mock,
        _ok_mock,  # _mock_stdout
    ):
        code = """from typing import List

bad_type: List[str] = 'tmp.txt'
"""

        test_file = Path(__file__).parent / "static_typing_test.py"
        with open(test_file, "w", encoding="utf-8") as fp:
            fp.writelines(code)

        staged_mock.return_value = [
            StatusEntry(
                status_string="M  static_typing_test.py",
                root_path=Path(__file__).parent,
            )
        ]

        ret = precommit()

        # Returncode != 0 -> errors
        self.assertEqual(1, ret)
        test_file.unlink()

    # these Terminal output functions don't run in the CI ...
    # @patch('sys.stdout', new_callable=StringIO)
    @patch("autohooks.plugins.mypy.mypy.ok")
    @patch("autohooks.plugins.mypy.mypy.out")
    @patch("autohooks.plugins.mypy.mypy.error")
    @patch("autohooks.plugins.mypy.mypy.get_staged_status")
    def test_precommit_ok(
        self,
        staged_mock,
        _error_mock,
        _out_mock,
        _ok_mock,  # _mock_stdout
    ):
        code = """from typing import List

bad_type: List[str] = ['tmp.txt']
"""

        test_file = Path(__file__).parent / "static_typing_test.py"
        with open(test_file, "w", encoding="utf-8") as fp:
            fp.writelines(code)

        staged_mock.return_value = [
            StatusEntry(
                status_string="M  static_typing_test.py",
                root_path=Path(__file__).parent,
            )
        ]

        ret = precommit()

        # Returncode 0 -> no errors
        self.assertEqual(0, ret)
        test_file.unlink()
