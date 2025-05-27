# LinOLS
LinOLS is a free, open-source chiptuning software, similar to WinOLS.

# LinOLS - Chiptuning Software

LinOLS is a free, open-source chiptuning software. It allows for advanced ECU mapping and remapping for tuning and optimization, similar to WinOLS. LinOLS is built with Python and provides a graphical user interface for easier interaction and visualization of data.

## Features

- Advanced ECU mapping and remapping
- Plotting and data visualization with `matplotlib`.
- Customizable to suit various ECU tuning needs.

## How to run LinOLS on Linux
You can download the `executable` for Linux, which is located under the `latest release` in this repository.

And then you just run it with `./LinOLS`.

## How to run LinOLS on Windows
You can download an `setup file` for Window 10/11 64bit in map called `Windows_Setup` in this repository. 

## Donations
You can donate here: `https://www.paypal.com/donate?hosted_button_id=HEKSD48J386MJ`
## Prerequisites

### System Requirements

- **Operating System**: Windows or Linux-based (Ubuntu, Arch, or other distributions).
- **Python 3**: Ensure Python 3.x is installed.
  - Check if Python is installed: `python3 --version`
  - If not installed, you can install it using your system package manager.

### Python Dependencies

- **matplotlib**: A plotting library for Python used for graphical representation.
  
  To install `matplotlib`, use `pip`:
  ```bash
  pip install matplotlib

- **pyqt6**: A GUI library for Python used for making GUI applications.
  
  To install `pyqt6`, use `pip`:
  ```bash
  pip install pyqt6

- **tkinter**: A GUI library for Python used for making GUI applications.

  To install `tkinter`, use your distro's `package manager`:
  
  Arch based distros:
  ```bash
  sudo pacman -S tk
  ```
  Ubuntu/Debian based distros:
  ```bash
  sudo apt install python3-tk
  ```
  Fedora based distros:
  ```bash
  sudo dnf install python3-tkinter
  ```
  
## How to run LinOLS
  When you installed all dependencies and they are working as intended you can run LinOLS using the following command:
  ```bash
  python3 main.py
```
## How to compile Cython files on Linux
  ### Required packages
  Before you start, ensure that you have the necessary packages installed. You can install `Cython` using pip:
  ```bash
  pip install Cython
  ```
  ### Compilation Steps
  Navigate to the `potential_maps` directory:
  ```bash
  cd potential_maps
  ```
  Then the following command to compile the Cython files:
  ```bash
  python setup.py build_ext --inplace
  ```
## How to compile Cython files on Windows
  ### Required packages
  Before you start, ensure that you have the necessary packages installed. You can install `Cython` using pip:
  ```bash
  pip install Cython
  ```
  You also have to install `Microsoft Build Tools`.
  
  ### Compilation Steps
  Navigate to the `potential_maps` directory:
  ```bash
  cd potential_maps
  ```
  Then the following command to compile the Cython files:
  ```bash
  python setup.py build_ext --inplace
  ```

## How to make an executable
  To make an Executable you have to use `pyinstaller` a Python library to make executables.
  You can install `pyinstaller` using `pip`:
  ```bash
  pip install pyinstaller
  ```
  Once you have pyinstaller installed you can run this command in the `"LinOLS directory"`:

  Linux:
  ```bash
  pyinstaller --onefile --windowed --hidden-import='PIL._tkinter_finder' --add-binary='potential_maps/find_maps.cpython-313-x86_64-linux-gnu.so:.' main.py
  ```
  Windows:
  ```bash
  pyinstaller --onefile --windowed --hidden-import='PIL._tkinter_finder' --add-binary='potential_maps/find_maps.cp313-win_amd64.pyd:.' --icon=icon.ico main.py
  ```

## Desktop Shortcut
  If you want you can use a provided template desktop shortcut named: `LinOLS.desktop`.
  New update
  You can also find an icon named: `icon.png`.

  Only thing you need to edit is `Exec` and `Icon`.

## Instructions
  ### Text Tab
  You can select multiple numbers with holding the `left click` and then draging with your mouse.

  You can select one value and right click on text widget to open a `context menu`.

  `Copy` is used for copying values into Excel or LibreCalc
  `Paste` is used for pasting values from Excel or LibreCalc into your file.
  `Undo` for undoing any changes.
  `Redo` for redoing any changes.
  `Open Map` - Open a map if the selected value is a map value.
  `Add Map` is used for adding a new map.
  `Text to 2D` is used to show where the selected value or values are in 2d mode.

  `Copy Hex Address` - Copies hex address of a selected value. 
  `Add Potential Map` - Adds a potential map to your user maps.
  `Remove Potential Map` - Removes a potential map from your project.
  
  You can use 'm'/'M' to increase number of columns by one or use 'w'/'W' to decrease the columns by one.
  
  You can use 'Page Up' and 'Page Down' for faster navigation.

  `Selected: #` label is for showing you how many numbers do you have selected currently

  `Columns: #` is used for showing the number of columns.

  `Shift: #` is used for showing the shift value which basicly moves every value for x times to the right.

  `Ori: #` label is for showing the original value of the selected value.

  #### Toolbar
  `|<<` is used for showing the first value.
  `<<` is used for showing a previous value.
  `|||` is used for opening a `Difference` dialog
  `>>` is used for showing a next value.
  `>>|` is used for showing the last value.

  `LOHI and HILO` are for chaning the byte order and changing the mode will ERASE any changes done.

  `Search icon` is used for opening the `Find` dialog.

  `Circled arrow` is used to open `Find Hex Address` dialog.

  `Column icons` are used as described in the description of each individual icon. The description can be accessed by hovering your mouse over the selected icon.


  ### 2D Tab
  You can select a number on 2d canva and you will automaticly show you that number in text mode.
  
  You can use 'Page Up' and 'Page Down' for faster navigation.
  
  `<` move one frame to the left.
  
  `>` move frame to the right.
  
  `<<` move a little bit to the left. 

  `>>` move a little bit to the left. 
  
  `Update` this will update 2d mode with the latest data from text mode.

  `Value: #` this will show you what value you have selected in 2d mode.

  `%` update location of the 2d mode to the one that is enetered in entry box.

  `-` and `+` increase or decrease the value by one.

  ### 3D Tab
  To select the values hold left click and drag over the values you want to select (doesn't work on axis).

  To rotate 3D plot hold left click and drag it around.
  
  You can right click on both axis and any map value to change the `axis's/map's properties`.

  You can quickly modify selected values by right-clicking on any map value. This will allow you to `sign map values in 3D` and `Value` -> used to change selected value quickly.

  Every copy and paste buttons are meant for interection with programs like `Excel` and `Libre Calc`.

  `Copy Map` copy the values of the map, including both axis to clipboard.

  `Copy Selected` is used to copy selected values to clipboard.
  
  `Update` is used to update values from text view to 3d view.

  `Diff: 0` Shows what is the change on the selected value.

  `Row and column boxes` are used to show current rows and columns in 3d view.
  
  `Ori: 0` Shows what is the original value of the selected value.

  `Write Map` is used to transfer values from 3d grid to text view, so update them.

  `Paste Selected` is used to paste values from clipboard to the location of the starting value / ONE selected value.

  `Paste Map` is used to paste the map to 3d grid, including both axis.

  ### Maps Tab
  `Maps Tab` is used to show all of the created or imported maps.

  You can `right click` on the map you want to remove. 

  ### File Menu
  `Open` - Open a new file.
  
  `Save` - Save everything into a new file.

  ### Options Menu
  `Find` can be used to find certain number in your file.

  `Import` is used to import already made file with the current one.

  `Difference` is used to show you diffrences done in your file.

  `Value Changes` is used to change multiple numbers at once.

  `Find Hex Address` is used to find your hex address in opened file.

  `Restart Map Search` is used to restart potential map search.

  ### Mappack Menu
  `Import Mappack` is used to import mappack / `.mp` files.

  `Export Mappack` is used to export mappack / `.mp` files.  

  ### Shortcuts
  Skip to the next changed value - `n`
  
  Ship to the previous changed value - `v`

  Ship to the first changed value - `e`

  Ship to the last changed value - `l`

  `Ctrl+Z` - undo
  
  `Ctrl+Y` - redo

  `Ctrl+U` - difference dialog

  `Ctrl+C` - copy selected
  
  `Ctrl+V` - paste selected

  `Ctrl+Shift+C` - copy whole map in `3D` tab
  
  `Ctrl+Shift+V` - paste whole map in `3D` tab
  
  `Ctrl+F` - find dialog

  `Ctrl+G` - find hex address dialog

  `Shift+5` - value changer dialog

  `w` - decrement number of columns by one

  `m` - increase number of columns by one

  `k` - add a new map

## Acknowledgments

Some icons/images used in this project are sourced from:

- **CleanPNG**: [https://www.cleanpng.com/](https://www.cleanpng.com/)
- **Heroicons**: [https://heroicons.com/](https://heroicons.com/) (licensed under the MIT License)
- **SVGrepo** : [https://www.svgrepo.com/](https://www.svgrepo.com/) (licensed under the MIT License)

### Modifications
- Some icons have been modified in terms of color and size to fit the design of this project.
