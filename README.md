# GameList XML Utilities

## Background
These Python scripts provide utilities for managing a `gamelist.xml` file, typically used in gaming systems to organize and display ROMs. The scripts help identify missing games, hide specific games, and manage unscraped game entries. They use `Typer` for command-line interaction and XML parsing to manipulate the `gamelist.xml` file effectively.

## Scripts Overview

### 1. `add_missing_games_and_hide.py`
#### Functionality
This script scans the ROM folder, identifies missing games that are not listed in `gamelist.xml`, and adds them with a `hidden` status. It also backs up the original `gamelist.xml` file before making any modifications.

#### Parameters
- `gamelist_dir` (str, required): The path to the directory containing `gamelist.xml`.
- `ignore_folders` (str, optional): A comma-separated list of subfolders to ignore during the scan.

#### Outputs
- A backup copy of `gamelist.xml`.
- A list of missing games saved to `#games_missing_in_gamelist.txt`.
- Updated `gamelist.xml` with missing games marked as hidden.

#### Example Usage
```sh
python add_missing_games_and_hide.py /path/to/games --ignore_folders "ignored_folder1,ignored_folder2"
```

---

### 2. `find_unscraped_games.py`
#### Functionality
This script scans the ROM folder and compares it with `gamelist.xml` to find:
- Games that are missing from the `gamelist.xml`.
- Games without an `<image>` tag.
- Games where the `<name>` tag starts with `ZZZ(notgame)`.

It then outputs lists of these games into text and batch files for further processing.

#### Parameters
- `rom_folder` (str, required): The path to the ROM folder.
- `find_missing` (bool, optional, default=True): Whether to find games missing in `gamelist.xml`.
- `find_no_image` (bool, optional, default=True): Whether to find games missing an `<image>` tag.
- `find_invalid_name` (bool, optional, default=True): Whether to find games with an invalid name format (`ZZZ(notgame)`).

#### Outputs
- A list of missing games (`#unscraped_games.txt`) and a batch script (`#move_unscraped_games.bat`) to move them.
- A list of games without images (`#games_without_images.txt`) and a batch script (`#move_games_without_images.bat`).
- A list of games with invalid names (`#games_invalid_names.txt`) and a batch script (`#move_games_invalid_names.bat`).

#### Example Usage
```sh
python find_unscraped_games.py /path/to/roms --find_missing True --find_no_image True --find_invalid_name True
```

---

### 3. `hide_games.py`
#### Functionality
This script hides games in `gamelist.xml` based on specific conditions:
- Games with names starting with `ZZZ(notgame)`.
- Games missing an `<image>` tag.
- The ability to ignore specific folders during processing.

It also creates a backup before modifying `gamelist.xml` and records hidden games in text files.

#### Parameters
- `gamelist_dir` (str, required): The directory containing `gamelist.xml`.
- `hide_zzz` (bool, optional, default=True): Whether to hide games that start with `ZZZ(notgame)`.
- `hide_no_image` (bool, optional, default=True): Whether to hide games missing an `<image>` tag.
- `ignore_folders` (str, optional): A comma-separated list of subfolders to ignore.

#### Outputs
- A backup copy of `gamelist.xml`.
- A list of games with invalid names saved to `#games_invalid_names.txt`.
- A list of games without images saved to `#games_without_images.txt`.
- An updated `gamelist.xml` with the selected games marked as hidden.

#### Example Usage
```sh
python hide_games.py /path/to/games --hide_zzz True --hide_no_image True --ignore_folders "ignored_folder1"
```

---

## Summary
These scripts provide an efficient way to manage `gamelist.xml`, ensuring missing games are tracked, unscraped games are identified, and unwanted games are hidden. They are useful for maintaining a clean and well-organized game library.

