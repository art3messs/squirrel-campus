"""
Data models and state tracking for the SquirrelCampus Engine.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class GameState:
    location: str = "The Main Quad Oak Tree"
    belly_fullness: int = 50
    agility: int = 50
    campus_notoriety: int = 10
    hoard: int = 0
    goal_hoard: int = 50
    turn: int = 1
    inventory: List[str] = field(default_factory=list)
    active_threat: Optional[str] = None
    game_over: bool = False
    victory: bool = False
    log: List[str] = field(default_factory=list)

    def clamp_stats(self):
        """Keep stats strictly within 0-100 bounds."""
        self.belly_fullness = max(0, min(100, self.belly_fullness))
        self.agility = max(0, min(100, self.agility))
        self.campus_notoriety = max(0, min(100, self.campus_notoriety))
        self.hoard = max(0, self.hoard)

        # Check win / lose conditions
        if self.hoard >= self.goal_hoard:
            self.victory = True
            self.game_over = True
        elif self.belly_fullness <= 0:
            self.game_over = True
            self.victory = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "location": self.location,
            "belly_fullness": self.belly_fullness,
            "agility": self.agility,
            "campus_notoriety": self.campus_notoriety,
            "hoard": self.hoard,
            "goal_hoard": self.goal_hoard,
            "turn": self.turn,
            "inventory": self.inventory,
            "active_threat": self.active_threat,
            "game_over": self.game_over,
            "victory": self.victory,
        }


@dataclass
class ActionResult:
    success: bool
    narrative: str
    fullness_delta: int = 0
    agility_delta: int = 0
    notoriety_delta: int = 0
    hoard_delta: int = 0
    item_acquired: Optional[str] = None
    escaped_threat: bool = False
