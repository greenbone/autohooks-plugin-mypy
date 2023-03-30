# Copyright 2021 Vincent Texier <vit@free.fr>
# Copyright 2023 Greenbone AG
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

import subprocess
import sys
from typing import Iterable, List, Optional, Tuple

from autohooks.api import error, ok, out
from autohooks.api.git import get_staged_status, stash_unstaged_changes
from autohooks.api.path import match
from autohooks.config import Config

DEFAULT_INCLUDE: Tuple[str] = ("*.py",)
DEFAULT_ARGUMENTS: List[str] = []


def check_mypy_installed() -> None:
    try:
        import mypy  # pylint: disable=import-outside-toplevel, disable=unused-import
    except ImportError as e:
        raise RuntimeError(
            "Could not find mypy. Please add mypy to your python environment"
        ) from e


def get_mypy_config(config: Config) -> Config:
    return config.get("tool").get("autohooks").get("plugins").get("mypy")


def ensure_iterable(value) -> Iterable[str]:
    if isinstance(value, str):
        return [value]

    return value


def get_include_from_config(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_INCLUDE

    mypy_config = get_mypy_config(config)
    include = ensure_iterable(mypy_config.get_value("include", DEFAULT_INCLUDE))

    return include


def get_mypy_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_ARGUMENTS

    mypy_config = get_mypy_config(config)
    arguments = ensure_iterable(
        mypy_config.get_value("arguments", DEFAULT_ARGUMENTS)
    )

    return arguments


# pylint: disable=unused-argument
def precommit(config: Optional[Config] = None, **kwargs) -> int:
    check_mypy_installed()
    include = get_include_from_config(config)

    files = [f for f in get_staged_status() if match(f.path, include)]

    if not files:
        ok("No staged files to check.")
        return 0

    arguments = get_mypy_arguments(config)

    with stash_unstaged_changes(files):
        ret = 0

        absolute_path_files = list(map(lambda p: str(p.absolute_path()), files))

        cmd = ["mypy"]
        cmd.extend(arguments)
        cmd.extend(absolute_path_files)
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            ret = e.returncode
            error("Static typing error(s) found:")
            lint_errors = e.stdout.decode(
                encoding=sys.getdefaultencoding(), errors="replace"
            ).split("\n")
            # Skip the first line that only shows ******** Module blah
            for line in lint_errors:
                out(line)
            return ret

        ok("Mypy check was successful.")
        return ret
