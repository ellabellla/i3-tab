# I3 Tab
Adds simple alt tab functionality to i3.

Written by Ella Pash

## Usage
Press `alt+tab` to switch to the last window in focus. Continue holding `tab` to keep the menu up. Whilst in the menu press `shift` to move the selection backwards and `tab` to move the selection forwards. The selected window will be in bold.

A config file must be specified as a command line argument. A default config file can be found [here](./config/config.ini).
## Config
- window
  - color: text color
  - bcolor: background color
  - width: how many selections width is the menu
- selection
  - width: width of selection box
  - height: height of selection box
- font
  - selected: font string for selected text
  - unselected: font string for unselected text
  - a font string is formatted like "Font-Name Size Style..." 
    - e.g. "Any 10 bold" or "Helvetic 10 bold italic"

## Installation
First clone the repository:

```
git clone https://github.com/ellabellla/i3-tab.git
```

Then run the commands:

```
pip install i3ipc
pip install PySimpleGUI
pip install pynput

chmod +x path-to-i3-tab/i3-tab.py
```

Then add the following lines to your i3 config:
```
for_window [class="i3-tab"] floating enable sticky enable border none move position center 

exec path-to-i3-tab/i3-tab.py path-to-config/config.ini
```

## Dependencies
### General
- i3
- python
### Python
- i3ipc
- PySimpleGUI
- Pynput

## License
This code is licensed under the MIT license. View the license [here](LICENSE).