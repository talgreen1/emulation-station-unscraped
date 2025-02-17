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
    hide_zzz: bool = typer.Option(True, help="Hide games that start with 'ZZZ(notgame)'"),
    hide_no_image: bool = typer.Option(True, help="Hide games without an image tag"),
    ignore_folders: str = typer.Option(None, help="Comma-separated list of subfolders to ignore")
):
    """
      Hide games in a 'gamelist.xml' based on specific criteria and update the file. This function will:

    1. Create a backup of the original 'gamelist.xml' file.
    2. Hide games that start with 'ZZZ(notgame)' if the 'hide_zzz' option is True.
    3. Hide games that do not have an image tag if the 'hide_no_image' option is True.
    4. Optionally ignore specific subfolders while applying the hide filters.
    5. Write the names of hidden games (invalid name or no image) into text files.
    6. Update the 'gamelist.xml' file by marking the hidden games with a <hidden>true</hidden> tag.

    Args:
        gamelist_dir (str): The directory containing the 'gamelist.xml' file.
        hide_zzz (bool): Whether to hide games that start with 'ZZZ(notgame)'.
        hide_no_image (bool): Whether to hide games that lack an image tag.
        ignore_folders (str): A comma-separated list of subfolders to ignore when hiding games.

    Raises:
        typer.Exit: If the 'gamelist.xml' file is not found in the specified directory.
    """
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

    # Hide games that start with 'ZZZ(notgame)'
    invalid_name_games = []
    if hide_zzz:
        for game in root.findall("game"):
            name_elem = game.find("name")
            path_elem = game.find("path")
            if path_elem is not None and name_elem is not None and name_elem.text.strip().startswith(ZZZ_PREFIX):
                path = path_elem.text.strip().lstrip("./")
                if not any(folder in path for folder in ignore_folders_list):
                    hidden_elem = game.find("hidden")  # Check if the hidden element already exists
                    if hidden_elem is None:  # If it doesn't exist, create it
                        hidden_elem = ET.SubElement(game, "hidden")
                        hidden_elem.text = "true"
                    invalid_name_games.append(name_elem.text.strip())

    # Hide games without an image tag
    no_image_games = []
    if hide_no_image:
        for game in root.findall("game"):
            image_elem = game.find("image")
            path_elem = game.find("path")
            if image_elem is None or not image_elem.text.strip():
                if path_elem is not None:
                    path = path_elem.text.strip().lstrip("./")
                    if not any(folder in path for folder in ignore_folders_list):
                        hidden_elem = game.find("hidden")  # Check if the hidden element already exists
                        if hidden_elem is None:  # If it doesn't exist, create it
                            hidden_elem = ET.SubElement(game, "hidden")
                            hidden_elem.text = "true"
                        name_elem = game.find("name")
                        if name_elem is not None:
                            no_image_games.append(name_elem.text.strip())

    # Write the names of the hidden games to files
    if invalid_name_games:
        with open(gamelist_path.parent / INVALID_NAME_TXT, "w", encoding="utf-8") as txt_file:
            txt_file.write("\n".join(invalid_name_games))
        print(f"Found {len(invalid_name_games)} games with invalid names (starting with 'zzz').")
    if no_image_games:
        with open(gamelist_path.parent / NO_IMAGE_TXT, "w", encoding="utf-8") as txt_file:
            txt_file.write("\n".join(no_image_games))
        print(f"Found {len(no_image_games)} games without images.")

    # Write the modified gamelist.xml file
    tree.write(gamelist_path)

    typer.echo("gamelist.xml updated successfully.")

if __name__ == "__main__":
    typer.run(hide_games)
