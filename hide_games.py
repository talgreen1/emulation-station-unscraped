import shutil
import xml.etree.ElementTree as ET
import typer
import os
from pathlib import Path
from datetime import datetime

# Constants for output file names and directories

NO_IMAGE_TXT = "#games_without_images.txt"
INVALID_NAME_TXT = "#games_invalid_names.txt"


MISSING_GAMES_FOLDER = "missing_games"
NO_IMAGE_FOLDER = "no_image_games"
INVALID_NAME_FOLDER = "invalid_name_games"

ZZZ_PREFIX = "ZZZ(notgame)"

def hide_games(
    gamelist_path: str = typer.Argument(..., help="Path to the gamelist.xml file"),
    hide_zzz: bool = typer.Option(True, help="Hide games that start with 'ZZZ(notgame)'"),
    hide_no_image: bool = typer.Option(True, help="Hide games without an image tag")
):
    gamelist_path = Path(gamelist_path).resolve()
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

    # Hide games that start with 'ZZZ(notgame)'
    invalid_name_games = []
    if hide_zzz:
        for game in root.findall("game"):
            name_elem = game.find("name")
            if name_elem is not None and name_elem.text.strip().startswith(ZZZ_PREFIX):
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
            if image_elem is None or not image_elem.text.strip():
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