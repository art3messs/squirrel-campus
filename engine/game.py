"""
SquirrelCampus Core Game Loop and Decision Engine.
"""

from typing import Dict, Any, List, Tuple
from engine.models import GameState, ActionResult
from engine.threats import roll_random_threat, Threat
from engine.tools import (
    scavenge_for_food,
    execute_distraction,
    manage_winter_hoard,
    craft_trash_artifact,
)


class SquirrelGame:
    def __init__(self):
        self.state = GameState()
        self.current_threat: Threat | None = None

    def get_current_choices(self) -> List[Dict[str, Any]]:
        """
        Returns 3 punchy, humorous choices for the current turn.
        """
        if self.current_threat:
            return self.current_threat.maneuver_choices

        # Standard turn choices
        return [
            {
                "key": "A",
                "label": "Raid the Dining Hall Loading Dock (Greedy, high reward)",
                "tool": "scavenge_for_food",
                "args": {
                    "target_location": "DINING_HALL_LOADING_DOCK",
                    "forage_strategy": "GREEDY_CHEEK_STUFFER",
                    "consumption_intent": "FIFTY_FIFTY_SPLIT",
                },
            },
            {
                "key": "B",
                "label": "Steal an artisan pastry from Library Cafe Patio (Stealthy)",
                "tool": "scavenge_for_food",
                "args": {
                    "target_location": "LIBRARY_CAFE_PATIO",
                    "forage_strategy": "STEALTH_NIBBLER",
                    "consumption_intent": "EAT_IMMEDIATELY",
                },
            },
            {
                "key": "C",
                "label": "Pull off a power-pole backflip to bewilder a tour group",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "TOUR_GROUP_CROWD",
                    "maneuver_type": "PARKOUR_POWER_POLE_BACKFLIP",
                },
            },
        ]

    def advance_turn(self, choice_key: str) -> ActionResult:
        """
        Processes a player's choice, executes the underlying tool, updates state,
        and triggers threats every 3 turns.
        """
        choices = self.get_current_choices()
        selected = next((c for c in choices if c["key"].upper() == choice_key.upper()), None)
        if not selected:
            selected = choices[0]  # Fallback

        tool_name = selected["tool"]
        args = selected.get("args", {})

        # Execute corresponding tool with extracted stats
        if tool_name == "scavenge_for_food":
            result = scavenge_for_food(
                target_location=args.get("target_location", "THE_MAIN_QUAD_GRASS"),
                forage_strategy=args.get("forage_strategy", "SNATCH_AND_SPRINT"),
                consumption_intent=args.get("consumption_intent", "FIFTY_FIFTY_SPLIT"),
                current_fullness=self.state.belly_fullness,
                current_agility=self.state.agility,
                current_hoard=self.state.hoard,
            )
        elif tool_name == "execute_distraction":
            result = execute_distraction(
                target_entity=args.get("target_entity", "TIRED_COLLEGE_STUDENT"),
                maneuver_type=args.get("maneuver_type", "HYPNOTIC_TAIL_FLUFF_DANCE"),
                current_agility=self.state.agility,
                current_notoriety=self.state.campus_notoriety,
            )
        elif tool_name == "manage_winter_hoard":
            result = manage_winter_hoard(
                action=args.get("action", "BURY_DEEP_IN_ROOTS"),
                current_hoard=self.state.hoard,
                suspected_thief=args.get("suspected_thief", "NONE"),
            )
        elif tool_name == "craft_trash_artifact":
            result = craft_trash_artifact(
                crafting_recipe=args.get("crafting_recipe", "CRUSHED_ENERGY_DRINK_HELMET"),
                current_agility=self.state.agility,
            )
        else:
            result = ActionResult(success=True, narrative="You twitch your tail nervously.")

        # Apply stat deltas
        self.state.belly_fullness += result.fullness_delta
        self.state.agility += result.agility_delta
        self.state.campus_notoriety += result.notoriety_delta
        self.state.hoard += result.hoard_delta

        if result.item_acquired:
            self.state.inventory.append(result.item_acquired)

        # Natural digestion penalty per turn
        self.state.belly_fullness -= 4

        # Clamp and evaluate win/lose
        self.state.clamp_stats()

        # Resolve threat status
        if self.current_threat:
            self.current_threat = None
            self.state.active_threat = None

        # Increment turn
        self.state.turn += 1

        # Threat check every 3 turns
        if not self.state.game_over and (self.state.turn % 3 == 0):
            threat = roll_random_threat()
            self.current_threat = threat
            self.state.active_threat = threat.name

        return result
