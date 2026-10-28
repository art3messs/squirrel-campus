# 🐿️ SquirrelCampus Engine

> *"Survive the semester. Dodge the Frisbees. Conquer the Quad."*

Welcome to **SquirrelCampus Engine**! I built this project to combine two things I love: **unhinged emergent RPG gameplay** and **agentic LLM function calling architecture**. 

In SquirrelCampus, you don't play as a knight or a space marine. You play as an ambitious, hyperactive campus squirrel trying to survive an unforgiving college semester, out-scheme your arch-rival **Barnaby "One-Nut" McFluff**, and stash away 50 delicacies before the brutal winter frost sets in.

---

## 💡 Why I Built This

I wanted to design a game engine that bridges classic text-adventure RPG mechanics with modern **AI tool-calling specifications**. 

Instead of hardcoded, static text trees, every action—from raiding a dumpster behind Greek Row to executing an acrobatic mid-air backflip in front of a campus tour group—is modeled as a **structured tool call**. The game state dynamically calculates success rates, modifies stats with real risk/reward curves, and feeds structured output back into the narrative loop.

Whether you run it via the local **terminal CLI** or wire it up as a toolset for an LLM (like Google Gemini or Claude), the engine tracks state deterministically while keeping the narrative energetic, unpredictable, and hilarious.

---

## ✨ Features & Mechanics

### 📊 Dynamic Squirrel Stats (0–100)
- **Belly Fullness (`0–100`):** Your metabolic clock. Drop to 0 and you pass out behind a recycling bin (Game Over).
- **Agility (`0–100`):** Dictates your escape velocity and parkour success. *Caution:* Getting too full triggers **Chubby Squirrel Inertia**, lowering your agility!
- **Campus Notoriety (`0–100`):** How famous you are among humans. Low notoriety means students ignore or shoo you; high notoriety means students pull out their phones to film TikToks, creating huge distraction windows.
- **The Winter Hoard (`0 / 50`):** Your stash of acorns, bagel slices, and stolen croissant corners. Reach 50 to win the winter.

### 🛠️ Agentic Tool Ecosystem
I engineered 4 primary function-calling tools with full OpenAPI / Gemini compatible schemas located in [`schemas/tools.json`](schemas/tools.json):
1. **`scavenge_for_food`**: High-risk campus raids (Dorm Dumpsters, Library Cafe, Stadium Bleachers, Dining Hall Docks) with tactical strategies (`STEALTH_NIBBLER`, `GREEDY_CHEEK_STUFFER`, `SNATCH_AND_SPRINT`).
2. **`execute_distraction`**: Theatrical campus stunts (`THE_UNBLINKING_DEATH_STARE`, `PARKOUR_POWER_POLE_BACKFLIP`, `CHUTE_DIVE_BACKPACK_INFILTRATION`) executed against specific campus entities.
3. **`manage_winter_hoard`**: Anti-theft bunker tactics against rival thieves like Barnaby McFluff or groundskeepers.
4. **`craft_trash_artifact`**: MacGyver-style crafting from campus trash (`Crushed Energy Drink Helmet`, `Chewing Gum Claw Grippers`, `Chip Bag Hang Glider`).

### 🚨 Campus Threat System (Every 3 Turns)
Every 3 turns, the campus throws a chaotic hazard at you:
- **Professor Whiskers (The Campus Cat):** A tuxedo apex predator stalking the Quad.
- **The Ultimate Frisbee Cannonball:** A neon-pink plastic disc hurled at Mach 2.
- **The Groundskeeper's Riding Lawnmower:** An unyielding blade machine grinding acorns to dust.

---

## 🏗️ Architecture

```
squirrel-campus/
├── engine/
│   ├── __init__.py
│   ├── models.py        # GameState, ActionResult, and Stat clamping
│   ├── tools.py         # Deterministic tool solvers & stat-weighted RNG
│   ├── threats.py       # Threat tables & adaptive encounter generator
│   └── game.py          # Core game loop & turn orchestration
├── schemas/
│   └── tools.json       # Gemini / OpenAPI tool declarations for LLM agent integration
├── tests/
│   └── test_engine.py   # Full test coverage for mechanics & state transitions
├── main.py              # Interactive Rich-powered terminal interface
├── pyproject.toml       # Python package configuration
└── requirements.txt     # Dependencies (rich, pytest)
```

---

## 🚀 Getting Started

### 1. Clone & Setup
```bash
git clone git@github.com:art3messs/squirrel-campus.git
cd squirrel-campus
```

### 2. Install Dependencies
Using `uv` (recommended on Arch Linux):
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```
Or standard `pip`:
```bash
pip install -r requirements.txt
```

### 3. Run the Game
```bash
python main.py
```

### 4. Run the Tests
```bash
pytest tests/
```

---

## 🤖 Using as an LLM Toolset

You can plug [`schemas/tools.json`](schemas/tools.json) straight into any function-calling agent:

```python
import json
from engine.tools import scavenge_for_food, execute_distraction

# Load the schema into your agent
with open("schemas/tools.json") as f:
    tools_spec = json.load(f)

# When your LLM triggers a tool call:
if function_call.name == "scavenge_for_food":
    result = scavenge_for_food(**function_call.args)
    # Feed result.narrative back to your model!
```

---

## 🗺️ What's Next
- [ ] **Multiplayer Quad Wars:** Socket-based territory competition between rival squirrels.
- [ ] **Live Gemini Audio Stream:** Real-time commentary from an AI sports commentator tracking your squirrel stunts.
- [ ] **Weather Hazards:** Sleet, rainstorms, and autumn leaf piles affecting ground friction.

---

*Crafted with high agility, frantic chittering, and lots of caffeine by **art3messs**.*
