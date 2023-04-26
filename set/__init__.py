import enum
import itertools
import random
from typing import Iterable


class Color(enum.Enum):
    RED = 1
    GREEN = 2
    PURPLE = 3


class Shape(enum.Enum):
    DIAMOND = 1
    OVAL = 2
    SQUIGGLE = 3


class Fill(enum.Enum):
    EMPTY = 1
    STRIPED = 2
    SOLID = 3


class Number(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class SetCard:
    def __init__(self, color: Color, shape: Shape, fill: Fill, number: Number) -> None:
        self.color = color
        self.shape = shape
        self.fill = fill
        self.number = number

    def __repr__(self) -> str:
        return (
            f"{self.color.name} {self.shape.name} {self.fill.name} {self.number.name}"
        )


class Deck:
    def __init__(self, shuffled: bool = True) -> None:
        self.deck = []
        for color in Color:
            for shape in Shape:
                for fill in Fill:
                    for number in Number:
                        self.deck.append(SetCard(color, shape, fill, number))
        if shuffled:
            self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.deck)

    def draw(self, count: int = 3) -> set[SetCard]:
        return {self.deck.pop() for _ in range(count)}

    def __contains__(self, card: SetCard) -> bool:
        return card in self.deck

    def __iter__(self) -> Iterable[SetCard]:
        return iter(self.deck)

    def __repr__(self) -> str:
        return f"{self.deck}"

    def __len__(self) -> int:
        return len(self.deck)


class CardCollection:
    def __init__(self, cards: Iterable[SetCard] = None) -> None:
        self.cards = set(cards) if cards else {}

    def add(self, card: SetCard) -> None:
        self.cards.add(card)

    def extend(self, cards: Iterable[SetCard]) -> None:
        self.cards.update(cards)

    def remove(self, card: SetCard) -> None:
        self.cards.remove(card)

    def reduce(self, cards: Iterable[SetCard]) -> None:
        self.cards.difference_update(cards)

    def is_set(self, cards: Iterable[SetCard]) -> bool:
        if len(cards) != 3:
            return False
        return (
            sum(card.color.value for card in cards) % 3 == 0
            and sum(card.shape.value for card in cards) % 3 == 0
            and sum(card.fill.value for card in cards) % 3 == 0
            and sum(card.number.value for card in cards) % 3 == 0
        )

    def possible_sets(self) -> set[frozenset[SetCard]]:
        return {
            frozenset(set)
            for set in itertools.combinations(self.cards, 3)
            if self.is_set(set)
        }

    def set_count(self) -> int:
        return len(self.possible_sets())

    def __contains__(self, card: SetCard) -> bool:
        return card in self.cards

    def __iter__(self) -> Iterable[SetCard]:
        return iter(self.cards)

    def __repr__(self) -> str:
        return f"{self.cards}"

    def __len__(self) -> int:
        return len(self.cards)


class Game:
    def __init__(self, deck: Deck = None, in_play: CardCollection = None) -> None:
        self.deck = deck or Deck()
        self.in_play = in_play or CardCollection()
        self.found_sets: list[frozenset[SetCard]] = []

    def finished(self) -> bool:
        return len(self.deck) == 0 and len(self.in_play) == 0

    def replenish(self) -> None:
        while (self.in_play.set_count() == 0 or len(self.in_play) < 12) and len(
            self.deck
        ) > 0:
            self.in_play.extend(self.deck.draw())

    def find_set(self, cards: Iterable[SetCard]) -> bool:
        if self.in_play.is_set(cards):
            self.in_play.reduce(cards)
            self.found_sets.append(frozenset(cards))
            return True
        return False
