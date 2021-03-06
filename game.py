from typing import List

from copy import copy

PLAYER_X = 'X'
EMPTY_CELL = '_'
PLAYER_O = 'O'


class Cell:
    def __init__(self, pos):
        self.pos = pos
        self.data = {
            PLAYER_X: 0,
            PLAYER_O: 0
        }
        self.tables = 0

    def __iadd__(self, other):
        self.data[other] += 1
        return self

    def __str__(self):
        return "{}:({:.2f}; {:.2f}) ".format(
            self.pos,
            self.data[PLAYER_X] / self.tables,
            self.data[PLAYER_O] / self.tables,
        )


class Game:
    def __init__(self):
        self.tables = [Table()]  # type: List[Table]
        self.win_tables = []

    def tables_resort(self):
        tables = self.tables[:]
        self.tables = []
        for table in tables:
            if EMPTY_CELL != table.win():
                self.win_tables.append(table)
            else:
                self.tables.append(table)

    def step(self, player: int, positions: List[int]):
        new_tables = []

        for table in self.tables:
            for pos in positions:
                if not self.is_allowed(pos):
                    raise ValueError(
                        "Клетка {} заполнена, ход в неё невозможен".format(
                            pos))
                if table.is_empty(pos):
                    _t = copy(table)
                    _t.add_figure(player, pos)
                    new_tables.append(_t)

        if 0 == len(new_tables):
            raise ValueError("Fuck you, bad step")

        self.tables = new_tables

        self.tables_resort()

        if 0 == len(self.tables):
            raise ZeroDivisionError("You WIN!!!!!")

    def is_allowed(self, pos) -> bool:
        """ Нельзя ходить в полностью заполненную клетку рабочих """
        for table in self.tables:
            if table.is_empty(pos):
                return True
        return False

    @property
    def field(self) -> List[Cell]:
        field = [Cell(x) for x in range(9)]

        for table in self.tables:
            for pos, cell in table.cells:
                field[pos] += cell

        act_tables = len(self.tables)

        for cell in field:
            cell.tables = act_tables

        return field

    @property
    def winners(self):
        data = {
            PLAYER_X: 0,
            EMPTY_CELL: 0,
            PLAYER_O: 0,
            'tables': len(self.tables) + len(self.win_tables)
        }

        for table in self.win_tables:
            data[table.win()] += 1

        data[EMPTY_CELL] = len(self.tables)

        return data


win_tables = [
    # horisont
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    # vertical
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    # dyagonales
    (0, 4, 8),
    (2, 4, 6)
]


class Table:
    def __init__(self, table: 'Table' = None):
        self._data = copy(table._data) if table else [EMPTY_CELL for _ in range(9)]
        self._cache = None

    def add_figure(self, figure, pos) -> bool:
        if self.is_empty(pos):
            self._data[pos] = figure
            self._cache = None
            return True
        else:
            return False

    def _calc_empty_cache(self):
        self._cache = [EMPTY_CELL == cell for cell in self._data]

    def is_empty(self, pos):
        if self._cache is None:
            self._calc_empty_cache()

        return self._cache[pos]

    def win(self):
        for a, b, c in win_tables:
            if self._data[a] == self._data[b] == self._data[c]\
                    and self._data[a] is not None\
                    and self._data[a] != EMPTY_CELL:
                return self._data[a]
        return EMPTY_CELL

    @property
    def cells(self):
        for i, cell in zip(range(9), self._data):
            if cell != EMPTY_CELL:
                yield i, cell

    def __copy__(self) -> 'Table':
        return Table(self)

    def __str__(self):
        return "".join(self._data)
