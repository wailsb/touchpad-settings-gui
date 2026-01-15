# Touchpad Settings GUI

## Overview

This small GUI lets you control touchpad settings via `xinput` on X11. It is a GTK3 Python app (single-file `main.py`) that manipulates libinput properties through `xinput`.

## Requirements

- X11 session (the app uses `xinput` which targets X server devices)
- Python 3
- PyGObject (GTK3 bindings)
- `xinput` utility

On Wayland `xinput` may not work; use compositor-specific settings or native tools for Wayland sessions.

## Packages (by distribution)

- Debian / Ubuntu:
  - xinput (or x11-utils)
  - python3
  - python3-gi
  - gir1.2-gtk-3.0
  - python3-gi-cairo (optional)
- Fedora:
  - xorg-x11-utils or xinput
  - python3
  - python3-gobject
  - gtk3
- Arch Linux:
  - xorg-xinput
  - python
  - python-gobject
  - gtk3

## Install commands

Debian / Ubuntu:
```bash
sudo apt update
sudo apt install -y xinput python3 python3-gi gir1.2-gtk-3.0 python3-gi-cairo
```

Fedora:
```bash
sudo dnf install -y xorg-x11-utils xinput python3-gobject gtk3
```

Arch Linux:
```bash
sudo pacman -Syu --noconfirm xorg-xinput python python-gobject gtk3
```

If your distribution uses different package names, ensure you install `xinput`, PyGObject (python3-gi), and GTK3 bindings.

## Run the application

From the repository root or where `main.py` is located:
```bash
python3 /path/to/touchpad-settings-gui/main.py
```
Replace `/path/to/touchpad-settings-gui` with the absolute path to the project on your machine.

## Add to desktop applications (create a .desktop file)

Create `~/.local/share/applications/touchpad-settings-gui.desktop` with these contents (adjust `Exec` and `Icon` if needed):

```
[Desktop Entry]
Type=Application
Name=Touchpad Settings GUI
Comment=Manage touchpad settings via xinput
Exec=python3 /home/youruser/touchpad-settings-gui/main.py
Icon=input-touchpad
Terminal=false
Categories=Utility;Settings;
```

Steps:

1. Replace `/home/youruser/touchpad-settings-gui/main.py` with the actual absolute path to `main.py`.
2. Save the file to `~/.local/share/applications/`.
3. Optionally make `main.py` executable:
```bash
chmod +x /home/youruser/touchpad-settings-gui/main.py
```
4. Refresh your desktop menu or log out and log back in. The app should appear in your launcher.

For system-wide installation copy the repository to `/opt/touchpad-settings-gui` and place the `.desktop` file in `/usr/share/applications/` (requires root).

## Troubleshooting

- `xinput: command not found`: install the `xinput` package for your distribution.
- Running under Wayland: `xinput` operates on X11 devices and may not affect input on Wayland compositors.
- Permission issues: run the app in the same user X session; do not use `sudo` to run GUI apps in a different session.
- If widgets do not appear, ensure PyGObject and GTK3 bindings are installed.

## Minimal checklist

- [ ] Install system packages (`xinput`, PyGObject, GTK3)
- [ ] Run `python3 main.py` to test
- [ ] Create `.desktop` file in `~/.local/share/applications/` to add to your launcher

## Notes

The app calls `xinput` directly. On systems using Wayland, prefer compositor-native settings or tools that target libinput directly.
# This project is a small python Gui for Linux to manage touchpad settings using xinput

