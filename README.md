# LinOLS
LinOLS is a free, open-source chiptuning software, similar to WinOLS, designed for experienced users.

# LinOLS - Chiptuning Software

LinOLS is a free, open-source chiptuning software designed for experienced users. It allows for advanced ECU mapping and remapping for tuning and optimization, similar to WinOLS. LinOLS is built with Python and provides a graphical user interface for easier interaction and visualization of data.

## Features

- Advanced ECU mapping and remapping.
- User-friendly interface for experienced tuners.
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

- **tkinter**: A GUI libary for Python used for making gui applications.

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

- **zenity**: A package for Gnu/Linux distors used for making things like file dialogs.

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
  To make an Executable you have to use `pyinstaller` a Python libary to make executables.
  You can install `pyinstaller` using `pip`:
  ```bash
  pip install pyinstaller
  ```
  Once you have pyinstaller installed you can run this command in the `"LinOLS directory"`:
  ```bash
  pyinstaller --onefile --windowed --hidden-import='PIL._tkinter_finder' main.py
  ```
