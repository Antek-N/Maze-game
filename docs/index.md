# MazeGame

**MazeGame** is a lightweight 2D maze game built with **Python** and **Pygame**.  
Players navigate through designed mazes, collect time records, and progress through levels — all wrapped in a simple interface with logging, menu, timer, and user profiles.

It’s a showcase of **event-driven gameplay**, **collision handling**, and **menu-based UI logic** in Pygame.

> **License:** `CC0-1.0`
> **Requirements:** `Python 3.12–3.14`, `pygame`, `sqlite3`

---

## Features

- **Progressive maze levels**  
  Programmatically drawn layouts with increasing difficulty.

- **Profiles & local auth**  
  **Login / Register** flows stored in a local SQLite database.

- **Records & leaderboard**  
  Best times saved per user; simple **records board** view.

- **Timer & session flow**  
  Start → play → finish → results board → next level.

- **Collision handling**  
  Smooth movement with wall collision resolution utilities.

- **In-game menus**  
  Initial menu, pause menu, help, window settings.

- **Custom theming**  
  Bundled font (`segoeprb.ttf`) and background image.

---

## Requirements & Dependencies

- **Python:** 3.12–3.14  
- **Runtime libraries:**  
  `pygame` (2D engine), `pygame-menu`, `sqlite3`, `logging`
- **Dev (optional):**  
  `pytest`, `black`, `ruff`, `mypy`, `pre-commit`, `mkdocs`, `pyinstaller`

---

## Installation

### Using Poetry

**Users**
```bash
poetry install --without dev
poetry run mazegame
```

**Developers** (runtime + dev dependencies)
```bash
poetry install
poetry run mazegame
```

### Using pip

**Users**
```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
pip install -e .
mazegame
```

**Developers** (runtime + dev dependencies)
```bash
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
```

---

## Run (Quick Start)

```bash
python -m mazegame
```
or
```bash
poetry run mazegame
```

---

## Usage

### Menus & Screens
- **Initial / Login / Register** — pick or create a local profile.
- **Main Menu** — start game, open records, help, window settings.
- **Pause** — pause/resume mid-run.
- **Results Board** — review your time after finishing a level.

### Gameplay Loop
1. **Sign in** (or register) a local user.
2. **Start a level** and navigate the maze to the exit.
3. Your **finish time** is saved to the local records database.
4. **Advance** to the next level from the result board.

### Data Storage
- `assets/databases/accounts.db` — local users (credentials/profile).
- `assets/databases/records.db` — finish times and leaderboard entries.

---

## Project Structure

```
src/mazegame/
├─ __main__.py                 # Entry point
├─ app.py                      # Init, screen registry, launch first screen
├─ logging_config.py           # Color-aware UTC logging (console/file)
│
├─ assets/
│  ├─ databases/
│  │  ├─ accounts.db          # Profiles
│  │  └─ records.db           # Highscores
│  ├─ fonts/
│  │  └─ segoeprb.ttf         # UI font
│  └─ img/
│     ├─ icon.ico             # Windows icon
│     ├─ icon.png             # App icon
│     └─ theme.jpg            # Background/theme
│
├─ maze_creator/
│  ├─ draw_maze.py            # Render grid/tiles to surface
│  ├─ get_number_of_levels.py # Level count discovery
│  └─ levels.py               # Level definitions/layouts
│
├─ menu/
│  ├─ help.py                 # Help screen
│  ├─ initial_menu.py         # Initial screen
│  ├─ login.py                # Login
│  ├─ menu_when_login.py      # Main menu (logged in)
│  ├─ pause.py                # Pause view
│  ├─ records.py              # Records/leaderboard
│  ├─ register.py             # Registration
│  ├─ show_result_board.py    # Post-run results
│  ├─ window_settings.py      # Window size/settings
│  └─ menu_manager/
│     ├─ menu_manager.py      # Screen router
│     └─ set_screens.py       # Screen registry
│
├─ player/
│  └─ player.py               # Player entity & movement
│
└─ utils/
   ├─ collisions/
   │  ├─ collision_handling.py # Axis-aligned resolution
   │  └─ get_collision_list.py # Build collidable tiles list
   ├─ databases/
   │  └─ records_database.py   # Records CRUD
   ├─ display/
   │  ├─ create_display.py     # Init Pygame window
   │  └─ render_display.py     # Frame render & flip
   ├─ gameplay/
   │  ├─ events_handling.py    # Runtime input/event handling
   │  ├─ finish_handling.py    # Win/lose and end-of-level state
   │  ├─ open_new_level.py     # Level transitions
   │  └─ start_game.py         # Session setup & loop
   ├─ global_variables/
   │  └─ global_variables.py   # Shared state singleton
   ├─ paths/
   │  └─ paths.py              # Resource resolution (dev/pkg)
   ├─ save_records/
   │  └─ save_records.py       # Persist scores to DB
   └─ time/
      ├─ clock.py              # Tick helpers
      └─ convert_time.py       # Formatting/utilities
```

---

## Documentation

Local preview/build with **MkDocs**:

```bash
mkdocs serve      # http://127.0.0.1:8000
mkdocs build      # build static site
```

---

## Building a Windows Executable

Create a standalone `.exe` with **PyInstaller**:

```bash
pyinstaller Mazegame.spec
```
Artifacts will appear in `dist/`.

---

## API / Module Documentation

Full project documentation: **[API Reference -
mazegame](reference/mazegame/index.md)**.

------------------------------------------------------------------------

## License

This project is released under **CC0-1.0** (public domain).  
You may copy, modify, distribute, and use it commercially without additional permissions.
