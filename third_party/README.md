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

## Rebuilding with a modified pygame

The release provides `pygame-2.6.1.tar.gz`, the unchanged corresponding pygame
source, alongside the EXE and portable ZIP. Extract that archive, make your
changes, and build/install pygame into the project's Windows Python 3.12 virtual
environment using pygame's included build instructions. Then run `build.bat` to
rebuild the bridge against it. Do not rerun `setup.bat` afterward, as it installs
the pinned upstream version. The app source and build scripts are public here.
Modification for personal use and reverse engineering to debug modifications of
LGPL components are permitted under the applicable licenses.

The single-file EXE extracts its embedded libraries and notices temporarily.
The Licenses button opens those notices. The portable ZIP is also provided for
users who want the libraries unpacked beside the app. Python's included license
contains the additional Microsoft runtime terms applicable to Windows binaries.
