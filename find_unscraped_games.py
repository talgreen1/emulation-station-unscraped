import xml.etree.ElementTree as ET
import typer
import os
from pathlib import Path

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


def find_unscraped_games(
        rom_folder: str = typer.Argument(..., help="Path to the ROM folder to scan."),
        find_missing: bool = typer.Option(True, help="Find games not found in the gamelist."),
        find_no_image: bool = typer.Option(True, help="Find games without an <image> tag."),
        find_invalid_name: bool = typer.Option(True, help="Find games where <name> starts with 'ZZZ(notgame)'.")
):
    """
       Scans a given ROM folder and compares it against the `gamelist.xml` file to identify unsorted games.
       Outputs the results to text files and batch scripts for easy handling.

       Args:
           rom_folder (str): The path to the ROM folder that will be scanned for games.
           find_missing (bool): If True, finds games in the ROM folder that are missing in the gamelist.xml.
           find_no_image (bool): If True, finds games that do not have an <image> tag in the gamelist.xml.
           find_invalid_name (bool): If True, finds games where the <name> tag starts with 'ZZZ(notgame)'.

       Outputs:
           - A text file listing missing games (unscraped).
           - A batch file to move missing games to the `missing_games` folder.
           - A text file listing games without images.
           - A batch file to move games without images to the `no_image_games` folder.
           - A text file listing games with invalid names.
           - A batch file to move games with invalid names to the `invalid_name_games` folder.
       """
    rom_folder = Path(rom_folder).resolve()
    gamelist_path = rom_folder / "gamelist.xml"

    if not gamelist_path.exists():
        typer.echo("gamelist.xml not found in the specified folder.")
        raise typer.Exit(1)

    # Parse the gamelist.xml
    tree = ET.parse(gamelist_path)
    root = tree.getroot()

    # Get all scraped games from gamelist.xml
    scraped_games = set()
    games_without_images = set()
    games_with_invalid_names = set()

    for game in root.findall("game"):
        path_elem = game.find("path")
        image_elem = game.find("image")
        name_elem = game.find("name")

        if path_elem is not None:
            game_path = path_elem.text.strip().lstrip("./")
            scraped_games.add(game_path)
            if image_elem is None or not image_elem.text.strip():
                games_without_images.add(game_path)
            if name_elem is not None and name_elem.text.strip().startswith("ZZZ(notgame)"):
                games_with_invalid_names.add(game_path)

    # Get all ROM files in the folder
    all_roms = {file.name for file in rom_folder.iterdir() if
                file.is_file() and file.suffix.lower() not in {".xml", ".txt", ".bat"}}

    # Find games based on selected criteria
    missing_games = sorted(all_roms - scraped_games) if find_missing else []
    no_image_games = sorted(games_without_images) if find_no_image else []
    invalid_name_games = sorted(games_with_invalid_names) if find_invalid_name else []

    # Function to write results to files and move games
    def write_output(game_list, txt_filename, bat_filename, target_folder):
        if game_list:
            target_path = rom_folder / target_folder
            target_path.mkdir(exist_ok=True)
            with open(rom_folder / txt_filename, "w", encoding="utf-8") as txt_file:
                txt_file.write("\n".join(game_list))
            with open(rom_folder / bat_filename, "w", encoding="utf-8") as bat_file:
                for game in game_list:
                    bat_file.write(f"move \"{rom_folder / game}\" \"{target_path}\"\n")
            typer.echo(f"Found {len(game_list)} games. Output written to {txt_filename} and {bat_filename}.")

    # Write outputs for each category
    write_output(missing_games, UNSCRAPED_TXT, UNSCRAPED_BAT, MISSING_GAMES_FOLDER)
    write_output(no_image_games, NO_IMAGE_TXT, NO_IMAGE_BAT, NO_IMAGE_FOLDER)
    write_output(invalid_name_games, INVALID_NAME_TXT, INVALID_NAME_BAT, INVALID_NAME_FOLDER)


if __name__ == "__main__":
    typer.run(find_unscraped_games)