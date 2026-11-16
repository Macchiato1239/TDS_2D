# 2D Tower Defense
Link to repo: https://github.com/Macchiato1239/TDS_2D

About the game: A Python tower defense game built with Tkinter. Choose a difficulty, place towers
along the route, and stop enemies from reaching the base. It is quite a classic, but i did it mainly because it's a game i play with my friends a lot

## Contents

1. [Settings and running the game](#1-settings-and-running-the-game)
2. [How to play](#2-how-to-play)
3. [Game information](#3-game-information)
4. [Project structure](#4-project-structure)
5. [Tests](#5-tests)
6. [Exception handling](#6-exception-handling)
7. [Author notes](#7-author-notes)

## 1. Settings and running the game

### Requirements

- Python 3.10+.
- Tkinter, including the Tcl/Tk libraries. Tkinter is part of many Python
  installations, but some Linux and custom Python installations package it
  separately.

To check whether Tkinter is available, run:

```bash
python3 -m tkinter
```

If a small Tk window opens, Tkinter is ready. If the command fails, install the
Tkinter package provided for your operating system or use a Python distribution
that includes Tcl/Tk. 
If that still fails, then uh, you may have experience some other issues that i 
may not have encountered while developing and testing the game. So it's unfortunate "sad face"

### Start the game

Open a terminal in the project root, the folder containing `main.py`, and run:

```bash
python3 main.py
```
Or press the play button on top right if ur using VScode


## 2. How to play

1. On the main menu, click **Difficulty** to cycle through Normal, Hard, and
   Insane, then click **Play**.
2. Click one of the five tower cards in the hotbar to select it. Move the mouse
   over the map to preview its range.
3. Click a valid, unoccupied location to place the tower. Placement costs cash;
   towers cannot be placed on the path, spawn, base, or another occupied area.
4. Towers attack enemies that enter their range. Killing an enemy earns cash
   equal to its starting health. Enemies that reach the base damage it by their
   remaining health.
5. Farms pay their income when a wave is completed. There is a short break
   between waves, shown by the countdown.
6. Click a placed tower to select it, then press **X** to delete it. Press
   **Q** to cancel tower placement. Deleting a tower does not refund its cost.
7. Press **R** to pause or resume. While paused, use the overlay to resume,
   restart, or return to the main menu. **Escape** also resumes a paused game.
8. Win by completing every wave while keeping the base alive. If base health
   reaches zero, the game is lost. The result overlay offers restart and menu
   options. Click **Quit** on the main menu or press **S** to close the game.

The game starts with 750 cash and 100 base health. All five towers are available
in the hotbar from the start.

## 3. Game information

### 3.1 Enemies

Enemy **reward** is the cash earned for defeating it and equals its starting
health. If it reaches the base, it deals damage equal to its remaining health.
The speed values below are the values used by the game; higher values move
faster.

| Enemy | Health | Speed | Reward | Size (px) | Color |
| --- | ---: | ---: | ---: | ---: | --- |
| Normal | 6 | 0.5 | 6 | 20 × 20 | Light green (`#baff7d`) |
| Quick | 8 | 1.0 | 8 | 20 × 20 | Cyan (`#43adc4`) |
| Heavy | 30 | 0.4 | 30 | 25 × 25 | Gray teal (`#63838a`) |
| Abnormal | 12 | 0.5 | 12 | 22 × 22 | Green (`#7cb24d`) |
| Swift | 20 | 1.2 | 20 | 22 × 22 | Dark teal (`#145463`) |
| Elite abnormal | 150 | 0.5 | 150 | 27 × 27 | Dark green (`#076f00`) |
| Speedy Boss | 500 | 0.8 | 500 | 30 × 30 | Blue (`#005e94`) |
| Giant Boss | 2,000 | 0.2 | 2,000 | 35 × 35 | Black |

### 3.2 Towers

Range and size are measured in pixels. DPS is direct damage per second, computed
from damage per shot divided by the cooldown. Debuff damage is described
separately from direct DPS.

| Tower | Cost | Range | Size (px) | Damage / cooldown | Direct DPS | Ability |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| Soldier | 250 | 150 | 20 | 10 / 0.5 s | 20 | — |
| Freezer | 400 | 150 | 20 | 5 / 0.8 s | 6.25 | Slows enemies by 20% for 0.4 s per application. |
| Minigunner | 2,000 | 250 | 25 | 15 / 0.2 s | 75 | — |
| Farm | 200 | 10 | 20 | — | — | Pays 100 cash per completed wave. |
| Pyro | 500 | 80 | 20 | 2 / 0.6 s | 3.33 | Applies a burn dealing 3 damage every 0.5 s while active; burn duration is 20 s. |

## 4. Project structure

- `main.py` starts the application.
- `Head/` contains the `Game` state controller and Tkinter window setup.
- `States/` contains the menu, gameplay flow, pause, victory, and loss states.
- `Base/` contains shared game objects, including enemies, towers, buttons,
  projectiles, geometry, and custom exceptions.
- `Manager/` contains systems that coordinate towers, enemies, collisions,
  hotbar input, buildings, and display updates.
- `dictionary.py` stores enemy and tower definitions.
- `difficulty.py` defines the Normal, Hard, and Insane wave schedules.
- `Test/` contains the pytest suite and its test fixtures.

The game uses Tkinter for the window, canvas, and input events. `Game` changes
between high-level states, while `GameFlow` coordinates gameplay and delegates
work to the managers. Towers and enemies contain their own actions and effects;
the managers coordinate those objects and the game state.

## 5. Tests

I had multiple tests file and stored them in a test suite folder called Test,
i used fixture, pytest, try and catch, raise and pytest.raise() to for 
exception handling. I conducted the test in the main environment, not a virtual one
These are the lines i used for testing

```bash
python3 -m pip install pytest pytest-cov
```
Run the tests from the project root:
```bash
python3 -m pytest
```
One thing you may have noticed is that i did not use pytest, which i what i used for project 1,
but apparently pytest is not putting the project root on its import path, and therefore fails 
the tests immediately at the import lines. So i had to use the command above to directly give it
the project root and therefore, the project structures.

I also looked at the rubric and found out that the coverage of the test must be over 95%,
so i searched up how to see coverage percentage and learnt how to also generate a coverage 
markdown file, which i think is quite useful.
```bash
python -m pytest --cov=Base --cov=Manager --cov=States --cov=Head \
  --cov-report=term-missing \
  --cov-report=markdown:MarkDown/coverage.md
```

## 6. Exception handling

The game validates user and configuration data where it enters a manager or
dictionary. Errors are raised with context so invalid setup can be diagnosed.
During shutdown, a Tkinter cancellation error is ignored if its scheduled
callback has already been removed.

### 6.1 Built-in exceptions

| Exception | Where it is used |
| --- | --- |
| `AttributeError` | Reports missing fields in enemy or tower definitions. |
| `IndexError` | Reports a missing wave spawn entry or an enemy path index outside the path. |
| `KeyError` | Reports missing dictionary or difficulty entries; also serves as the base class for `UnknownDefinitionError`. |
| `ModuleNotFoundError` | Caught by `main.py` to show a startup message when a project module cannot be imported. |
| `NotImplementedError` | Marks the abstract status-effect update method as unimplemented. |
| `SystemExit` | Stops startup with the import error message when a required project module is unavailable. |
| `tkinter.TclError` | Caught during game cleanup if Tk has already removed the scheduled callback. |
| `TypeError` | Reports values of the wrong type, such as nonnumeric time or coordinates, unhashable IDs, or nonnumeric burn ticks. |
| `ValueError` | Reports invalid values or malformed wave/path data; also serves as the base class for several custom exceptions. |

### 6.2 Custom exceptions

These exceptions are defined in `Base/exceptions.py`. They inherit from built-in
exceptions, so existing handlers for the parent type can still catch them.

| Custom exception | Base class | Purpose |
| --- | --- | --- |
| `InvalidDifficultyError` | `ValueError` | The difficulty number is not one of the supported modes: Normal, Hard, or Insane. |
| `InvalidWaveDataError` | `ValueError` | A wave entry or path point does not have the expected structure. |
| `UnknownDefinitionError` | `KeyError` | An enemy or tower ID is not present in its dictionary. |
| `InvalidTowerConfigurationError` | `ValueError` | A tower definition uses an unsupported tower type. |

## 7. Author notes

If you looked into the previous commits, the initial name of the project is plant-and-bees, this is inspired by my friend who is also doing an oop project that has actual characters and world building in them.
But i changed the project to simply tower defense, which is rather basic, this is mainly because i faced many difficulties while trying to implement the game core functions and had to keep modifying its structures. 
Due to the difficulties of the project that i put myself on, i decided to strip the project of its world building so that i can focus on the technical side of it. If i had more time, i would have gotten into world building and make the towers and enemies more balanced, interesting. Initially i also made more than 3 tower types and intended to implement buff for enemies, but i supposed that would be scope creep for what the purpose of this project.
Even though it's a hard lesson to learn, i believe that with better time management and a less tight deadline, implementing both the system and then refining plus adding world building can be possible.
---
I also want to talk about what i have learnt.
The biggest lesson is probably refining the structure of the game too late into the project. Particularly, i spent 2 days on the project building enemy and tower system, i could make enemy run along the path and place tower down. At that point i haven't made projectile nor make the tower shoot yet. The problem here is that i put most of the code functions inside one class, the "game" class and put that class inside main.py. This definitely violates the first principle of **SOLID**, and perhaps some others, but i only noticed it when the project became harder to manage and code starts to look very ugly.
It took me 6 hours to split the game class into appropriately smaller classes. Even though the refinement made the code look much better, i believe that it can be improved, its just that i am too far into the project to do anything about it now.
If i were to start this project all again or start another project, i would start by implenting the most basic functions of the project and put them inside different classes, and each of them should handle only one responsibility.
---
One thing i also learnt is **type hinting**, even though its not in the rubric, i noticed my friend Jack who was working on his project. Jack used type hinting and docstring for every single attributes or functions. It looks beautiful. I spent an hour on adding type hinting to my projects. Even though it doesn't affect the code, i think it serves to maintain and manage the code better for further development.
