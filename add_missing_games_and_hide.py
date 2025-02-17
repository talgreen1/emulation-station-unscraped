import shutil
import xml.etree.ElementTree as ET
import typer
import os
from pathlib import Path
from datetime import datetime

# Constants for output file names and directories

NO_IMAGE_TXT = "#games_without_images.txt"
INVALID_NAME_TXT = "#games_invalid_names.txt"
MISSING_GAMES_TXT = "#games_missing_in_gamelist.txt"

MISSING_GAMES_FOLDER = "missing_games"
NO_IMAGE_FOLDER = "no_image_games"
INVALID_NAME_FOLDER = "invalid_name_games"

ZZZ_PREFIX = "ZZZ(notgame)"

def hide_games(
    gamelist_dir: str = typer.Argument(..., help="Path to the directory containing gamelist.xml"),
    ignore_folders: str = typer.Option(None, help="Comma-separated list of subfolders to ignore")
):

    gamelist_path = Path(gamelist_dir).resolve() / "gamelist.xml"
    if not gamelist_path.exists():
        typer.echo("gamelist.xml not found in the specified folder.")
        raise typer.Exit(1)

    # Create a backup of the gamelist.xml file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = gamelist_path.parent / f"{gamelist_path.stem}_backup_{timestamp}.xml"
    shutil.copy(gamelist_path, backup_path)

    # Parse the original gamelist.xml file
    tree = ET.parse(gamelist_path)
    root = tree.getroot()

    ignore_folders_list = [folder.strip() for folder in ignore_folders.split(",")] if ignore_folders else []

    # Get existing game paths
    existing_games = {game.find("path").text.strip().lstrip("./") for game in root.findall("game") if game.find("path") is not None}

    # Hide games that are missing from gamelist.xml
    missing_games = []

    # Filter ROM files and exclude those in the ignore_folders list
    rom_files = {
        file.relative_to(gamelist_dir).as_posix()
        for file in Path(gamelist_dir).rglob('*')
        if file.is_file() and file.suffix in [".zip", ".7z", ".nes", ".sfc", ".gba"] and
        not any(str(file.relative_to(gamelist_dir).parent).startswith(ignored_folder) for ignored_folder in ignore_folders_list)
    }

    missing_roms = rom_files - existing_games
    for rom in missing_roms:
        game_elem = ET.SubElement(root, "game")
        path_elem = ET.SubElement(game_elem, "path")
        path_elem.text = f"./{rom}"  # This ensures the subfolder is preserved
        hidden_elem = ET.SubElement(game_elem, "hidden")
        hidden_elem.text = "true"
        name_elem = ET.SubElement(game_elem, "name")
        name_elem.text = rom
        missing_games.append(rom)

    if missing_games:
        with open(gamelist_path.parent / MISSING_GAMES_TXT, "w", encoding="utf-8") as txt_file:
            txt_file.write("\n".join(missing_games))
        print(f"Found {len(missing_games)} missing games that were added and hidden.")

    # Write the modified gamelist.xml file
    tree.write(gamelist_path)

    typer.echo("gamelist.xml updated successfully.")

if __name__ == "__main__":
    typer.run(hide_games)
