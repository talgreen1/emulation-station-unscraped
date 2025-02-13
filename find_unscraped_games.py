import xml.etree.ElementTree as ET
import typer
import os
from pathlib import Path


def find_unscraped_games(
        rom_folder: str = typer.Argument(..., help="Path to the ROM folder to scan."),
        output_txt: str = typer.Option("unscraped_games.txt", help="Output text file listing unscraped games."),
        output_bat: str = typer.Option("move_unscraped_games.bat", help="Batch file to move unscraped games."),
        move_folder: str = typer.Option("unscraped", help="Folder where unscraped games will be moved.")
):
    rom_folder = Path(rom_folder).resolve()
    gamelist_path = rom_folder / "gamelist.xml"
    move_folder_path = rom_folder / move_folder

    if not gamelist_path.exists():
        typer.echo("gamelist.xml not found in the specified folder.")
        raise typer.Exit(1)

    # Parse the gamelist.xml
    tree = ET.parse(gamelist_path)
    root = tree.getroot()

    # Get all scraped games from gamelist.xml
    scraped_games = {game.find("path").text.strip().lstrip("./") for game in root.findall("game") if
                     game.find("path") is not None}

    # Get all ROM files in the folder
    all_roms = {file.name for file in rom_folder.iterdir() if
                file.is_file() and file.suffix.lower() not in {".xml", ".txt", ".bat"}}

    # Find games without scraped data
    unscraped_games = sorted(all_roms - scraped_games)

    if not unscraped_games:
        typer.echo("All games have scraped data. No files to move.")
        return

    # Write to text file
    with open(output_txt, "w", encoding="utf-8") as txt_file:
        txt_file.write("\n".join(unscraped_games))

    # Write batch file
    with open(output_bat, "w", encoding="utf-8") as bat_file:
        bat_file.write(f"mkdir \"{move_folder_path}\"\n")
        for game in unscraped_games:
            bat_file.write(f"move \"{rom_folder / game}\" \"{move_folder_path}\"\n")

    typer.echo(f"Found {len(unscraped_games)} unscraped games. Output written to {output_txt} and {output_bat}.")


if __name__ == "__main__":
    typer.run(find_unscraped_games)