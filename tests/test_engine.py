"""
Unit tests for SquirrelCampus Engine.
"""

from engine.game import SquirrelGame
from engine.models import GameState
from engine.tools import (
    scavenge_for_food,
    execute_distraction,
    manage_winter_hoard,
    craft_trash_artifact,
)


def test_initial_state():
    game = SquirrelGame()
    assert game.state.location == "The Main Quad Oak Tree"
    assert game.state.belly_fullness == 50
    assert game.state.agility == 50
    assert game.state.campus_notoriety == 10
    assert game.state.hoard == 0
    assert not game.state.game_over


def test_stat_clamping():
    state = GameState(belly_fullness=150, agility=-20, campus_notoriety=200, hoard=-5)
    state.clamp_stats()
    assert state.belly_fullness == 100
    assert state.agility == 0
    assert state.campus_notoriety == 100
    assert state.hoard == 0


def test_scavenge_tool():
    res = scavenge_for_food(
        target_location="LIBRARY_CAFE_PATIO",
        forage_strategy="STEALTH_NIBBLER",
        consumption_intent="FIFTY_FIFTY_SPLIT",
        current_fullness=50,
        current_agility=50,
        current_hoard=5,
    )
    assert isinstance(res.narrative, str)
    assert "chitter" in res.narrative or "scurry" in res.narrative or "patio" in res.narrative.lower()


def test_distraction_tool():
    res = execute_distraction(
        target_entity="TIRED_COLLEGE_STUDENT",
        maneuver_type="PARKOUR_POWER_POLE_BACKFLIP",
        current_agility=80,
        current_notoriety=20,
    )
    assert isinstance(res.success, bool)
    assert len(res.narrative) > 0


def test_turn_progression_and_threat():
    game = SquirrelGame()
    assert game.state.turn == 1

    # Advance to turn 2
    game.advance_turn("A")
    assert game.state.turn == 2
    assert game.current_threat is None

    # Advance to turn 3 - threat should trigger!
    game.advance_turn("B")
    assert game.state.turn == 3
    assert game.current_threat is not None
    assert game.state.active_threat is not None
