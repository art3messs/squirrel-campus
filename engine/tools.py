"""
Function tools and outcome calculators for SquirrelCampus Engine.
"""

import random
from engine.models import ActionResult


def scavenge_for_food(
    target_location: str,
    forage_strategy: str,
    consumption_intent: str,
    current_fullness: int,
    current_agility: int,
    current_hoard: int,
) -> ActionResult:
    """
    Simulates a food forage run based on location risk, strategy, and stats.
    """
    location_yield = {
        "DORM_DUMPSTER_ALLEY": (15, 25, 0.70),  # (min_food, max_food, base_success_rate)
        "LIBRARY_CAFE_PATIO": (10, 20, 0.85),
        "FOOTBALL_STADIUM_BLEACHERS": (12, 28, 0.75),
        "THE_MAIN_QUAD_GRASS": (5, 12, 0.95),
        "DINING_HALL_LOADING_DOCK": (20, 35, 0.60),
        "GREEK_ROW_PORCH": (15, 30, 0.65),
        "SCIENCE_LAB_GREENHOUSE": (8, 16, 0.90),
        "COMMUTER_PARKING_LOT": (6, 14, 0.80),
    }

    min_food, max_food, base_chance = location_yield.get(
        target_location, (8, 15, 0.80)
    )

    # Strategy modifiers
    if forage_strategy == "STEALTH_NIBBLER":
        success_chance = base_chance + 0.15
        yield_multiplier = 0.8
        notoriety_delta = 2
    elif forage_strategy == "GREEDY_CHEEK_STUFFER":
        success_chance = base_chance - 0.15
        yield_multiplier = 1.4
        notoriety_delta = 8
    else:  # SNATCH_AND_SPRINT
        success_chance = base_chance + (current_agility / 200)
        yield_multiplier = 1.0
        notoriety_delta = 4

    roll = random.random()
    if roll <= success_chance:
        raw_loot = int(random.randint(min_food, max_food) * yield_multiplier)
        
        # Distribute based on consumption intent
        if consumption_intent == "EAT_IMMEDIATELY":
            fullness_gain = min(raw_loot, 30)
            hoard_gain = 0
            narrative = (
                f"You scurry into {target_location.replace('_', ' ')} with a twitchy tail! "
                f"You unearth a glorious bounty of discard snacks and gorge immediately. "
                f"Your belly swells (+{fullness_gain} fullness), chittering in culinary bliss!"
            )
        elif consumption_intent == "HAUL_TO_HOARD":
            fullness_gain = -5  # Physical exertion costs energy
            hoard_gain = max(2, raw_loot // 4)
            narrative = (
                f"With cheeks stretched to cartoonish proportions, you carry a prime stash back from "
                f"{target_location.replace('_', ' ')}. The winter hoard grows by {hoard_gain} items!"
            )
        else:  # FIFTY_FIFTY_SPLIT
            fullness_gain = min(raw_loot // 2, 20)
            hoard_gain = max(1, raw_loot // 6)
            narrative = (
                f"A balanced raid! You scurry through {target_location.replace('_', ' ')}, "
                f"gobbling half on the spot (+{fullness_gain} fullness) and squirreling away "
                f"+{hoard_gain} nuts in your secret oak knot."
            )

        # High fullness slightly reduces agility (chubby squirrel inertia)
        agility_delta = -3 if (current_fullness + fullness_gain) > 75 else 0

        return ActionResult(
            success=True,
            narrative=narrative,
            fullness_delta=fullness_gain,
            agility_delta=agility_delta,
            notoriety_delta=notoriety_delta,
            hoard_delta=hoard_gain,
        )
    else:
        # Failure scenario
        return ActionResult(
            success=False,
            narrative=(
                f"Disaster in {target_location.replace('_', ' ')}! You were spotted by a grumpy custodian "
                f"wielding an oversized broom. You scamper up the nearest drainpipe with empty cheeks!"
            ),
            fullness_delta=-8,  # burn calories fleeing
            agility_delta=+2,   # reflex practice
            notoriety_delta=+5,
            hoard_delta=0,
        )


def execute_distraction(
    target_entity: str,
    maneuver_type: str,
    current_agility: int,
    current_notoriety: int,
) -> ActionResult:
    """
    Resolves a theatrical stunt or distraction against humans or predators.
    """
    difficulty_by_target = {
        "TIRED_COLLEGE_STUDENT": 35,
        "PROFESSOR_WHISKERS_CAMPUS_CAT": 65,
        "BARNABY_RIVAL_SQUIRREL": 50,
        "GROUNDSKEEPER_LAWNMOWER": 60,
        "TOUR_GROUP_CROWD": 40,
        "CAMPUS_SECURITY_GUARD": 45,
    }

    target_dc = difficulty_by_target.get(target_entity, 50)
    score_roll = random.randint(1, 100) + (current_agility * 0.4) + (current_notoriety * 0.2)

    if score_roll >= target_dc:
        notoriety_boost = random.randint(8, 15)
        narrative_stunt = (
            f"Spectacular execution! With a frantic tail-twitch, you execute {maneuver_type.replace('_', ' ')} "
            f"right in front of {target_entity.replace('_', ' ')}. "
            f"They freeze in utter bewilderment while onlookers gasp and pull out their smartphones! "
            f"(Campus Notoriety +{notoriety_boost})"
        )
        return ActionResult(
            success=True,
            narrative=narrative_stunt,
            fullness_delta=-3,
            agility_delta=+3,
            notoriety_delta=notoriety_boost,
            escaped_threat=True,
        )
    else:
        narrative_fail = (
            f"Oof! Your {maneuver_type.replace('_', ' ')} fell totally flat. "
            f"{target_entity.replace('_', ' ')} was unimpressed and lunged toward you. "
            f"You execute an emergency panic-scurry up a gutter!"
        )
        return ActionResult(
            success=False,
            narrative=narrative_fail,
            fullness_delta=-6,
            agility_delta=-2,
            notoriety_delta=-2,
            escaped_threat=False,
        )


def manage_winter_hoard(
    action: str,
    current_hoard: int,
    suspected_thief: str = "NONE",
) -> ActionResult:
    """
    Protects, relocates, or inspects the winter hoard.
    """
    if action == "BURY_DEEP_IN_ROOTS":
        saved = min(current_hoard, 5)
        return ActionResult(
            success=True,
            narrative=(
                f"You dig frantic little trenches beneath the roots of the Main Oak. "
                f"Your hoard of {current_hoard} snacks is now deeply camouflaged under autumn foliage."
            ),
            fullness_delta=-4,
            agility_delta=+1,
            hoard_delta=+1,  # Found an old buried acorn while digging!
        )
    elif action == "FORTIFY_TREE_HOLLOW":
        return ActionResult(
            success=True,
            narrative=(
                f"You pack pinecone wedges and sticky tree sap into the hollow. "
                f"Thieves like {suspected_thief.replace('_', ' ')} will find nothing but splintery agony!"
            ),
            fullness_delta=-5,
            agility_delta=+2,
        )
    elif action == "SET_DECOY_STASH":
        return ActionResult(
            success=True,
            narrative=(
                f"Diabolical genius! You plant hollow pebble shells in plain sight. "
                f"Barnaby and the campus crows will waste hours cracking decoy rocks!"
            ),
            fullness_delta=-3,
            notoriety_delta=+6,
        )
    else:
        return ActionResult(
            success=True,
            narrative=f"You inspect the stash. {current_hoard} items safely accounted for. Tail-twitch of satisfaction!",
            fullness_delta=-1,
        )


def craft_trash_artifact(
    crafting_recipe: str,
    current_agility: int,
) -> ActionResult:
    """
    Assembles campus litter into high-tier squirrel gear.
    """
    check = random.randint(1, 100) + (current_agility * 0.5)
    if check > 45:
        gear_name = crafting_recipe.replace("_", " ").title()
        return ActionResult(
            success=True,
            narrative=(
                f"With hyper-dexterous claw movements and a sharp chitter, you assemble the [{gear_name}]! "
                f"You strap it on, feeling like the undisputed kingpin of the campus trees."
            ),
            agility_delta=+5,
            notoriety_delta=+10,
            item_acquired=gear_name,
        )
    else:
        return ActionResult(
            success=False,
            narrative="You got your head stuck in a sticky soda can lid! You shake it off after vigorous head-shaking.",
            fullness_delta=-4,
            agility_delta=-2,
            notoriety_delta=+2,
        )
