import enum as _enum


class OutputColorScheme(_enum.Enum):
    """Different color scheme modes for the terminal."""

    RANDOM = _enum.auto()
    GRADIENT = _enum.auto()


class OutputColors:
    """A custom iterable collection for colors in the terminal."""

    def __init__(self, *args) -> None:
        if any(not isinstance(arg, str) for arg in args):
            raise ValueError("Every argument can to be of type str")

        self.arr = args
        self.index = 0

    def __getitem__(self, index) -> str:
        return self.arr[index]

    def __next__(self) -> str:
        self.index += 1
        if self.index == len(self.arr):
            self.index = 0

        return self.arr[self.index]

    def __len__(self) -> int:
        return len(self.arr)
