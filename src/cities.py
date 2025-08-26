from typing import TypedDict, List


class Local(TypedDict):
    city: str
    country: str


cities: List[Local] = [
    ("Brasília", "BR"),
    ("Rio de Janeiro", "BR"),
    ("São Paulo", "BR")
]
