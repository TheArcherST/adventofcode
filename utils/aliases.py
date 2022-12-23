from typing import TypeVar, Protocol, Iterator

from decimal import Decimal


ScalarAlias = TypeVar('ScalarAlias', int, float, Decimal)


class CoordinatesAlias(Protocol):
    def __getitem__(self, item: int) -> ScalarAlias: ...
    def __iter__(self) -> Iterator[ScalarAlias]: ...


def is_scalar(o: ScalarAlias):
    return isinstance(o, (int, float, Decimal))
