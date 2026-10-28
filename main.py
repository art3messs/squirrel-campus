#!/usr/bin/env python3
"""
SquirrelCampus Engine - Interactive Terminal CLI
"""

import sys
from engine.game import SquirrelGame

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import BarColumn, Progress, TextColumn
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def print_banner():
    banner = r"""
  ___              _              _  _____                                     
 / _ \            (_)            | |/ ____|                                    
| (_  | _   _  ___ _ _ __ _ __ __| | |     __ _ _ __ ___  _ __  _   _ ___     
 \__  || | | |/ _ \ | '__| '__/ _` | |    / _` | '_ ` _ \| '_ \| | | / __|    
 (___/ || |_| |  __/ | |  | | | (_| | |___| (_| | | | | | | |_) | |_| \__ \    
       \_______/\___|_|_|  |_|  \__,_|\_____\__,_|_| |_| |_| .__/ \__,_|___/    
                                                           | |                 
                                                           |_|                 
    """
    print(banner)
    print("Survival of the Fluffiest - College Edition\n" + "=" * 60)


def display_status(game: SquirrelGame):
    state = game.state
    if HAS_RICH:
        console = Console()
        table = Table(title=f"🐿️ SQUIRREL STATS - Turn {state.turn}", style="green")
        table.add_column("Location", style="cyan")
        table.add_column("Belly Fullness", style="magenta")
        table.add_column("Agility", style="yellow")
        table.add_column("Notoriety", style="red")
        table.add_column("The Hoard (Goal: 50)", style="bold green")

        table.add_row(
            state.location,
            f"{state.belly_fullness}/100 🥪",
            f"{state.agility}/100 ⚡",
            f"{state.campus_notoriety}/100 😎",
            f"{state.hoard}/50 🌰",
        )
        console.print(table)
        if state.active_threat:
            console.print(Panel(f"[bold red]⚠️ ACTIVE THREAT: {state.active_threat}![/bold red]", border_style="red"))
        if state.inventory:
            console.print(f"[dim]Gear: {', '.join(state.inventory)}[/dim]")
    else:
        print(f"\n--- SQUIRREL STATS [Turn {state.turn}] ---")
        print(f"Location: {state.location}")
        print(f"Belly: {state.belly_fullness}/100 | Agility: {state.agility}/100 | Notoriety: {state.campus_notoriety}/100 | Hoard: {state.hoard}/50")
        if state.active_threat:
            print(f"⚠️ THREAT DETECTED: {state.active_threat}!")
        if state.inventory:
            print(f"Gear: {', '.join(state.inventory)}")
        print("-" * 40)


def main():
    print_banner()
    game = SquirrelGame()

    print("\nThe crisp autumn breeze rustles through the Grand Oak.")
    print("Students shuffle to class, dropping half-eaten pastries, while your rival Barnaby McFluff")
    print("glares from the high branches. Winter is coming. Collect 50 snacks to survive!\n")

    while not game.state.game_over:
        display_status(game)
        choices = game.get_current_choices()

        print("\nChoose your maneuver:")
        for c in choices:
            print(f"  [{c['key']}] {c['label']}")

        user_input = input("\nYour action (A/B/C or Q to quit) > ").strip().upper()
        if user_input == "Q":
            print("\nYou scurry into your tree hollow and take a long squirrel nap. Game exited.")
            sys.exit(0)

        if user_input not in ["A", "B", "C"]:
            print("Invalid reflex! You froze and twitched your nose.")
            continue

        result = game.advance_turn(user_input)
        print("\n" + "=" * 50)
        print(f"🎲 OUTCOME: {result.narrative}")
        print("=" * 50)

    # End game resolution
    display_status(game)
    if game.state.victory:
        print("\n🎉 VICTORY! Your winter hoard reaches 50 bountiful delicacies!")
        print("You will feast like a king while Barnaby shivers on frozen pine needles.")
    else:
        print("\n💀 DEFEAT! Your belly hit 0 and you passed out from hunger behind a recycling bin.")
        print("Better luck next semester!")


if __name__ == "__main__":
    main()
