from dataclasses import dataclass


@dataclass
class Counter:
    id: int
    key: str
    title: str
    max_val: int | None
    value: int | None


@dataclass
class Stat:
    id: int
    key: str
    title: str
    min_val: int
    max_val: int
    median: int


@dataclass
class User:
    id: int
    name: str
