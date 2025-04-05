from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._length = 0
        self._table_size = 8
        self._threshold_factor = 2 / 3
        self._table: list = [None] * self._table_size

    @property
    def _threshold(self) -> int:
        return int(self._table_size * self._threshold_factor)

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        return str(self._table)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._length + 1 >= self._threshold:
            self._resize()
        self._insert(key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self._find_key(key)
        return self._table[index][1]

    def _resize(self) -> None:
        old_table = self._table
        self._table_size *= 2
        self._table: list = [None] * self._table_size
        self._length = 0

        for entry in old_table:
            if entry is not None:
                self._insert(*entry)

    def _insert(self, key: Any, value: Any) -> None:
        index = self._probe(key)
        if self._table[index] is None:
            self._length += 1
        self._table[index] = key, value

    def _find_key(self, key: Any) -> int:
        start_index = hash(key) % self._table_size
        for i in range(self._table_size):
            index = (start_index + i) % self._table_size
            entry = self._table[index]
            if entry is None:
                continue
            if entry[0] == key and hash(entry[0]) == hash(key):
                return index
        raise KeyError

    def _probe(self, key: Any) -> int:
        start_index = hash(key) % self._table_size
        for i in range(self._table_size):
            index = (start_index + i) % self._table_size
            if (self._table[index] is None
                    or (self._table[index][0] == key
                        and hash(self._table[index][0]) == hash(key))):
                return index
        raise RuntimeError
