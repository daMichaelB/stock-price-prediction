from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class SymbolDataDaily(object):
    adj_close: str
    date: str


@dataclass
class SymbolData(object):
    date: List[str] = field(default_factory=list)
    adj_close: List[str] = field(default_factory=list)
