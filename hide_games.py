import xml.etree.ElementTree as ET
import typer
import os
from pathlib import Path
from datetime import datetime

def hide_games(
    gamelist_path: str = typer.Argument(..., help="Path to the gamelist.xml file"),
    hide_zzz: bool = typer.Option(False, help="Hide games that start with 'ZZZ(notgame)'"),
    hide_no_image: bool = typer.Option(False, help="Hide games without an image tag")
):
    gamelist_path = Path(gamelist_path).resolve()
    if not gamelist_path.exists():
        typer.echo("gamelist.xml not found in the specified folder.")
        raise typer.Exit(1)

    # Create a copy of the original gamelist.xml file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_gamelist_path = f"{gamelist_path}.original_{timestamp}"
    os.rename(gamelist_path, original_gamelist_path)

    # Parse the original gamelist.xml file
    tree = ET.parse(original_gamelist_path)
    root = tree.getroot()

    # Hide games that start with 'ZZZ(notgame)'
    if hide_zzz:
        for game in root.findall("game"):
            name_elem = game.find("name")
            if name_elem is not None and name_elem.text.strip().startswith("ZZZ(notgame)"):
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