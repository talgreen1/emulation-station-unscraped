# Find Unscraped ROMs

## Overview
This script scans a folder containing ROM files and identifies games that meet specific conditions:
1. **Missing from gamelist.xml** – ROMs that are not listed in `gamelist.xml`.
2. **Without an image** – Games listed in `gamelist.xml` but missing an `<image>` tag.
3. **Invalid names** – Games whose `<name>` tag starts with `ZZZ(notgame)`.

For each category, the script generates:
- A `.txt` file listing the affected ROMs.
- A `.bat` file that moves these ROMs into category-specific folders.

## Installation
Ensure you have Python installed (version 3.6 or later). Install the required package:
```sh
pip install typer
```

## Usage
Run the script using the following command:
```sh
python find_unscraped_roms.py <path_to_rom_folder>
```
Optional flags:
- `--find-missing` (default: `True`): Find games missing from `gamelist.xml`.
- `--find-no-image` (default: `True`): Find games without an `<image>` tag.
- `--find-invalid-name` (default: `True`): Find games with names starting with `ZZZ(notgame)`.

Example usage:
```sh
python find_unscraped_roms.py "C:\path\to\roms" --find-no-image False
```
This will find missing and invalid name games but skip checking for games without images.

## Output
The script generates the following files in the ROM folder:

| Category | TXT File | BAT File | Destination Folder |
|----------|------------|------------|-----------------|
| Missing from gamelist | `unscraped_games.txt` | `move_unscraped_games.bat` | `missing_games/` |
| Without an image | `games_without_images.txt` | `move_games_without_images.bat` | `no_image_games/` |
| Invalid names | `games_invalid_names.txt` | `move_games_invalid_names.bat` | `invalid_name_games/` |

## How It Works
1. Parses `gamelist.xml` to get all listed games.
2. Compares against actual ROM files in the folder.
3. Identifies games in each category and generates corresponding TXT and BAT files.
4. Runs `.bat` files to move affected games to their respective folders.

## Notes
- The script does **not** delete any files, only moves them.
- Ensure `gamelist.xml` is present in the ROM folder before running the script.
- The output files and folders are automatically created.

## License
This script is free to use and modify. Contributions are welcome!