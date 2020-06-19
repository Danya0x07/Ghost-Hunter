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

from collections import deque
from abc import ABCMeta, abstractmethod

class PoolableObject(metaclass=ABCMeta):
    """
    Базовый класс для объектов, поддерживающих повторное использование
    без пересоздавания.
    """
    
    pool = deque()

    @classmethod
    def create(cls, *args):
        if len(cls.pool) == 0:
            return cls(*args)
        else:
            obj = cls.pool.pop()
            obj.reset(*args)
            return obj

    def delete(self, group):
        group.remove(self)
        self.pool.append(self)

    @abstractmethod
    def reset(self, *args):
        pass
