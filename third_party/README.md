# Third-party notices

Stadia Bridge's MIT license covers its original source. Bundled dependencies retain
their own licenses; the notices in this directory accompany the executable.

- Python 3.12.10: https://www.python.org/downloads/release/python-31210/
- pygame 2.6.1 (LGPL): https://github.com/pygame/pygame/tree/2.6.1
  Source: https://github.com/pygame/pygame/archive/refs/tags/2.6.1.tar.gz
  SDL and other pygame dependency notices are copied from that tag's docs/licenses.
- vgamepad 0.1.0 (MIT): https://github.com/yannbouteiller/vgamepad
  The exact source URL and checksum are in install_dependencies.py. Only its
  automatic launch of the old ViGEmBus installer is disabled; runtime code and
  ViGEmClient DLLs are unchanged.
- ViGEmClient (MIT): https://github.com/nefarius/ViGEmClient
- PyInstaller 6.11.1: https://github.com/pyinstaller/pyinstaller/tree/v6.11.1
  Its license includes the bootloader exception permitting application distribution.

The portable package uses dynamically loaded libraries in _internal. They are not
statically linked into the application. Source and build scripts for the bridge
are in the repository. The ViGEmBus driver installer is not included in the ZIP.
