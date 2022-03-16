# I3 Tab
Adds simple alt tab functionality to i3.

Written by Ella Pash

## Usage

Press `alt+tab` to switch to the last window in focus. Continue holding `tab` to keep the menu up. Whilst in the menu press `shift` to move the selection backwards and `tab` to move the selection forwards. The selected window will be in bold.

## Installation

Run the commands:

```
pip install i3ipc
pip install PySimpleGUI
pip install pynput

chmod +x path-to-i3-tab/i3-tab.py
```

Then add the following lines to your i3 config:
```
for_window [class="i3-tab"] floating enable sticky enable border none move position center 

exec path-to-i3-tab/i3-tab.py
```

## Dependencies
### General
- i3
### Python
- i3ipc
- PySimpleGUI
- Pynput

## License
This code is licensed under the MIT license. View the license [here](LICENSE).