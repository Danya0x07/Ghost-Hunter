# Copyright (C) 2019-2020, Daniel Efimenko
#
# This file is part of Haunted_Library.
#
# Haunted_Library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Haunted_Library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Haunted_Library.  If not, see <https://www.gnu.org/licenses/>.
#

# Таймеры общего назначения

class RegularTimer:
    """Таймер регулярного повторения."""

    def __init__(self, handler, timeout):
        self.handler = handler
        self.timeout = timeout
        self.counter = 0

    def update(self, delta, args=()):
        if self.counter >= self.timeout:
            self.counter = 0
            self.handler(*args)
        else: self.counter += delta


class CountdownTimer:
    """Таймер обратного отсчёта."""

    def __init__(self, handler, timeout):
        self.handler = handler
        self.counter = timeout

    def update(self, delta, args=()):
        if self.counter > 0:
            self.handler(*args)
            self.counter -= delta

    def restart(self, new_timeout):
        self.counter = new_timeout
