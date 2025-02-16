import shutil
import xml.etree.ElementTree as ET
import typer
import os
from pathlib import Path
from datetime import datetime

# Constants for output file names and directories
UNSCRAPED_TXT = "#unscraped_games.txt"
UNSCRAPED_BAT = "#move_unscraped_games.bat"
NO_IMAGE_TXT = "#games_without_images.txt"
NO_IMAGE_BAT = "#move_games_without_images.bat"
INVALID_NAME_TXT = "#games_invalid_names.txt"
INVALID_NAME_BAT = "#move_games_invalid_names.bat"

MISSING_GAMES_FOLDER = "missing_games"
NO_IMAGE_FOLDER = "no_image_games"
INVALID_NAME_FOLDER = "invalid_name_games"

ZZZ_PREFIX = "ZZZ(notgame)"

def hide_games(
    gamelist_path: str = typer.Argument(..., help="Path to the gamelist.xml file"),
    hide_zzz: bool = typer.Option(False, help="Hide games that start with 'ZZZ(notgame)'"),
    hide_no_image: bool = typer.Option(False, help="Hide games without an image tag")
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
    if hide_zzz:
        for game in root.findall("game"):
            name_elem = game.find("name")
            if name_elem is not None and name_elem.text.strip().startswith(ZZZ_PREFIX):
                game.set("hidden", "true")

    # Hide games without an image tag
    if hide_no_image:
        for game in root.findall("game"):
            image_elem = game.find("image")
            if image_elem is None or not image_elem.text.strip():
                game.set("hidden", "true")

    # Write the modified gamelist.xml file
    tree.write(gamelist_path)

    typer.echo("gamelist.xml updated successfully.")

if __name__ == "__main__":
    typer.run(hide_games)