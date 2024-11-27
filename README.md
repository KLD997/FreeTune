# LinOLS
LinOLS is a free, open-source chiptuning software, similar to WinOLS.

# LinOLS - Chiptuning Software

LinOLS is a free, open-source chiptuning software. It allows for advanced ECU mapping and remapping for tuning and optimization, similar to WinOLS. LinOLS is built with Python and provides a graphical user interface for easier interaction and visualization of data.

## Features

- Advanced ECU mapping and remapping
- Plotting and data visualization with `matplotlib`.
- Customizable to suit various ECU tuning needs.

## Prerequisites

### System Requirements

- **Operating System**: Linux-based (Ubuntu, Arch, or other distributions).
- **Python 3**: Ensure Python 3.x is installed.
  - Check if Python is installed: `python3 --version`
  - If not installed, you can install it using your system package manager.

### Required Dependencies

#### Python Dependencies

- **matplotlib**: A plotting library for Python used for graphical representation.
  
  To install `matplotlib`, use `pip`:
  ```bash
  pip install matplotlib

- **customtkinter**: A GUI library for Python used for making GUI applications.
  
  To install `customtkinter`, use `pip`:
  ```bash
  pip install customtkinter

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
#### Other Dependencies

- **zenity**: A package for Gnu/Linux distros used for making things like file dialogs.

  To install `zenity`, use your distro's `package manager`:
  
  Arch based distros:
  ```bash
  sudo pacman -S zenity
  ```
  Ubuntu/Debian based distros:
  ```bash
  sudo apt install zenity
  ```
  Fedora based distros:
  ```bash
  sudo dnf install zenity
  ```
## How to run LinOLS
  When you installed all dependencies and they are working as intended you can run LinOLS using the following command:
  ```bash
  python3 main.py
```
## How to make an executable
  To make an Executable you have to use `pyinstaller` a Python library to make executables.
  You can install `pyinstaller` using `pip`:
  ```bash
  pip install pyinstaller
  ```
  Once you have pyinstaller installed you can run this command in the `"LinOLS directory"`:
  ```bash
  pyinstaller --onefile --windowed --hidden-import='PIL._tkinter_finder' main.py
  ```
## Desktop Shortcut
  If you want you can use a provided template desktop shortcut named: `LinOLS.desktop`.
  
  You can also find an icon named: `icon.png`.

  Only thing you need to edit is `Exec` and `Icon`.

## Instructions
  ### Text Tab
  You can select multiple numbers with holding the `left click` and then draging with your mouse. You can only drag from up to down.

  `16-bit Lo-Hi and 16-Bit Hi-Lo` are for chaning the byte order and changing the mode will ERASE any changes done.

  `Selected: #` button is for showing you how many numbers do you have selected currently

  `Columns box` is used for changing the number of columns.

  `Shift box` is used for changing the shift value which basicly moves every value for x times to the right.

  `Text to 2D` is used to show where the selected value or values are in 2d mode.

  `Copy` is used for copying values into Excel or LibreCalc

  `Paste` is used for pasting values from Excel or LibreCalc into your file.

  `Undo` for undoing any changes.

  `Redo` for redoing any changes.

  ### 2D Tab
  You can select a number on 2d canva and you will automaticly show you that number in text mode.
  
  `<` move one frame to the left.
  
  `>` move frame to the right.
  
  `<<` move a little bit to the left. 

  `>>` move a little bit to the left. 
  
  `Update` this will update 2d mode with the latest data from text mode.

  `Value: #` this will show you what value you have selected in 2d mode.

  `%` update location of the 2d mode to the one that is enetered in entry box.

  `-` and `+` increase or decrease the value by one.

  ### File Menu
  `Open` - Open a new file.
  
  `Save` - Save everything into a new file.

  ### Options Menu
  `Find` can be used to find certain number in your file.

  `Import` is used to import already made file with the current one.

  `Difference` is used to show you diffrences done in your file.

  `Value Changes` is used to change multiple numbers at once.
  
  ### Shortcuts
  Edit mode - E
  
  Value Dialog - Shift + 5 (Can be accessible via Options menu)
