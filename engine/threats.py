"""
Threat encounters and campus hazard generator.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import random


@dataclass
class Threat:
    id: str
    name: str
    description: str
    maneuver_choices: List[Dict[str, Any]]


CAMPUS_THREATS = [
    Threat(
        id="CAMPUS_CAT",
        name="Professor Whiskers (The Campus Cat)",
        description="A sleek tuxedo feline with predatory eyes prowling silently beneath the maple branches.",
        maneuver_choices=[
            {
                "key": "A",
                "label": "Claw up the stone building wall",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "PROFESSOR_WHISKERS_CAMPUS_CAT",
                    "maneuver_type": "PARKOUR_POWER_POLE_BACKFLIP",
                },
            },
            {
                "key": "B",
                "label": "The Unblinking Death Stare from a low branch",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "PROFESSOR_WHISKERS_CAMPUS_CAT",
                    "maneuver_type": "THE_UNBLINKING_DEATH_STARE",
                },
            },
            {
                "key": "C",
                "label": "Panic scurry through the thorny rose bushes",
                "tool": "scavenge_for_food",
                "args": {
                    "target_location": "THE_MAIN_QUAD_GRASS",
                    "forage_strategy": "SNATCH_AND_SPRINT",
                    "consumption_intent": "HAUL_TO_HOARD",
                },
            },
        ],
    ),
    Threat(
        id="ROGUE_FRISBEE",
        name="The Ultimate Frisbee Cannonball",
        description="A neon-pink plastic disc comes hurtling spinning through the air directly at your skull!",
        maneuver_choices=[
            {
                "key": "A",
                "label": "Mid-air acrobatic tail-whip dodge",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "TIRED_COLLEGE_STUDENT",
                    "maneuver_type": "PARKOUR_POWER_POLE_BACKFLIP",
                },
            },
            {
                "key": "B",
                "label": "Play dead dramatically on the lawn",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "TOUR_GROUP_CROWD",
                    "maneuver_type": "DRAMATIC_PLAY_DEAD",
                },
            },
            {
                "key": "C",
                "label": "Dive headfirst into a discarded backpack",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "TIRED_COLLEGE_STUDENT",
                    "maneuver_type": "CHUTE_DIVE_BACKPACK_INFILTRATION",
                },
            },
        ],
    ),
    Threat(
        id="LAWNMOWER_DEATH_MACHINE",
        name="Groundskeeper's Aggressive Riding Lawnmower",
        description="A roaring green monster spitting grass clippings and obliterating all fallen acorns in its wake!",
        maneuver_choices=[
            {
                "key": "A",
                "label": "High-speed roof gutter leap",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "GROUNDSKEEPER_LAWNMOWER",
                    "maneuver_type": "PARKOUR_POWER_POLE_BACKFLIP",
                },
            },
            {
                "key": "B",
                "label": "Aggressive chittering from the safety of a copper lamppost",
                "tool": "execute_distraction",
                "args": {
                    "target_entity": "GROUNDSKEEPER_LAWNMOWER",
                    "maneuver_type": "HYPNOTIC_TAIL_FLUFF_DANCE",
                },
            },
            {
                "key": "C",
                "label": "Sprint and salvage shredded bagels before the mower blades arrive",
                "tool": "scavenge_for_food",
                "args": {
                    "target_location": "THE_MAIN_QUAD_GRASS",
                    "forage_strategy": "SNATCH_AND_SPRINT",
                    "consumption_intent": "HAUL_TO_HOARD",
                },
            },
        ],
    ),
]


def roll_random_threat() -> Threat:
    """Selects a random campus threat."""
    return random.choice(CAMPUS_THREATS)
