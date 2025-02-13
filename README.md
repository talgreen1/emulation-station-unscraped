

**gamelist_utils README**
==========================

**Project Overview**
-------------------

gamelist_utils is a Python script designed to help manage and organize game data by identifying unscraped games in a ROM folder. The script uses the `gamelist.xml` file to determine which games have already been scraped and compares this list to the actual ROM files in the folder. It then generates a text file and a batch file to help move the unscraped games to a designated folder.

**Usage**
---------

To use gamelist_utils, follow these steps:

1. **Install dependencies**: Make sure you have Python installed on your system. The script also uses the `typer` library, which can be installed using pip: `pip install typer`.
2. **Prepare your ROM folder**: Ensure that your ROM folder contains the `gamelist.xml` file and the ROM files you want to scan.
3. **Run the script**: Execute the script using Python: `python gamelist_utils.py`.
4. **Provide input**: The script will prompt you to provide the following inputs:
	* `rom_folder`: The path to the ROM folder to scan.
	* `output_txt`: The output text file listing unscraped games (default: `unscraped_games.txt`).
	* `output_bat`: The batch file to move unscraped games (default: `move_unscraped_games.bat`).
	* `move_folder`: The folder where unscraped games will be moved (default: `unscraped`).
5. **Review output**: The script will generate the output text file and batch file. Review the output to ensure that the unscraped games are correctly identified and the batch file is correct.

**Examples**
------------

Here are some examples of how to use the script:

* **Basic usage**: `python gamelist_utils.py --rom_folder /path/to/rom/folder`
* **Custom output files**: `python gamelist_utils.py --rom_folder /path/to/rom/folder --output_txt my_unscraped_games.txt --output_bat my_move_unscraped_games.bat`
* **Custom move folder**: `python gamelist_utils.py --rom_folder /path/to/rom/folder --move_folder my_unscraped_folder`

**Troubleshooting**
-----------------

If you encounter any issues while running the script, check the following:

* Ensure that the `gamelist.xml` file is present in the ROM folder.
* Verify that the ROM files are in the correct format and are not corrupted.
* Check the output text file and batch file for any errors or inconsistencies.

**License**
----------

gamelist_utils is released under the MIT License. See the LICENSE file for details.

**Contributing**
---------------

Contributions to gamelist_utils are welcome. If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository.