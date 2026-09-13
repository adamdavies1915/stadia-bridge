# Stadia Bridge

A Windows desktop application that reads one Google Stadia controller and exposes
it as a virtual Xbox 360 controller through XInput. Includes automatic connection
and reconnection, Start/Stop, adjustable radial stick deadzone, and live output.
The bridge continues while minimized. Closing it removes the virtual controller.

## Download and run

Download **StadiaBridge-0.1.0-Windows-x64.zip** from
[Releases](https://github.com/adamdavies1915/stadia-bridge/releases/latest), extract
all files, and run **StadiaBridge.exe**. Keep the `_internal` folder beside it.
No Python installation is needed. Windows 10/11 x64 and
[ViGEmBus](https://github.com/nefarius/ViGEmBus/releases/latest) are required.

Connect your Stadia controller, then keep the app open while playing. Minimized
is fine. Run only one instance. See `QUICKSTART.txt` in the ZIP for setup steps.

## Run from source

1. Install **Python 3.12, 64-bit**, including its launcher, from
   [python.org](https://www.python.org/downloads/windows/).
2. Install the signed **ViGEmBus** driver from the
   [maintainer's GitHub releases](https://github.com/nefarius/ViGEmBus/releases/latest).
   Restart Windows if the installer requests it. Administrator access is needed
   for driver installation; the bridge itself runs as a normal user.
3. Copy this project to Windows and double-click `setup.bat`. Internet access is
   needed for the Python dependencies. Setup verifies the vgamepad 0.1.0 source
   archive checksum and disables only its obsolete bundled driver installer before
   building the package. Its controller runtime and DLLs are unchanged.
4. Connect the Stadia controller using a USB data cable, or pair it in Windows
   Bluetooth settings if it **already has Bluetooth-enabled firmware**.
5. Double-click `start.bat`. The app starts bridging automatically when it finds
   the first device with “Stadia” in its name. Keep only one copy running.
6. Click **Test in Windows**, select **Controller (XBOX 360 For Windows)** (the
   exact name can vary), then open Properties. Check buttons, both sticks, and
   triggers. Open your game while the bridge is running.

## Xbox One versus Xbox 360

ViGEmBus supports Xbox 360 and DualShock 4 virtual devices, not an Xbox One device.
Xbox 360 output supplies standard XInput buttons, both sticks, and independent
analog triggers for compatible Windows games. An Xbox One label would not add
hardware features to a Stadia controller. This app does not forward vibration,
audio, headset functions, the Assistant button, or Capture button. SDL maps the
Stadia button to Guide and the menu buttons to Start/Back where supported by the
controller firmware. Some games or Windows overlays intercept Guide.

## Duplicate input and troubleshooting

Windows may show both the physical Stadia controller and the virtual Xbox device.
If a game responds twice, turn off other controller translators, including Steam
Input for that game when using this bridge. If the game still reads both devices,
[HidHide](https://github.com/nefarius/HidHide) can hide the physical device:

1. Add the bridge executable to HidHide's Applications allowlist. For a source
   launch this is the project's `.venv\Scripts\python.exe`; for a packaged build
   use `StadiaBridge.exe`.
2. On Devices, select **only the physical Stadia controller**, then enable device
   hiding. Leave the virtual Xbox controller visible.
3. Reconnect the controller and restart the bridge and game. If detection stops,
   disable hiding and check that the correct bridge executable was allowed.

If the app is waiting, check its Detected list, the USB cable/Bluetooth pairing,
and HidHide settings. If it reports a driver error, install/reinstall ViGEmBus,
restart Windows, and reopen the app. Logs are in
`%LOCALAPPDATA%\StadiaBridge\bridge.log`, accessible with **Open logs**.
Stop/close the app to release all inputs. Unplugging the controller releases all
inputs and removes the virtual controller; plugging it back in recreates it.
Unexpected driver/read errors stop the bridge and show an error; press Start to
retry. A recreated virtual device may need the game to be restarted.

**Dependency status:** [ViGEmBus is retired](https://github.com/nefarius/ViGEmBus)
and no longer maintained. Use the maintainer's signed release. Driver installation
is separate from this app; it is not silently installed by the bridge.

## Build an executable

On Windows, run `setup.bat`, then `build.bat`. The result is
`dist\StadiaBridge\StadiaBridge.exe`. Copy the **whole StadiaBridge folder** to the
target Windows 10/11 x64 PC; Python is then unnecessary, but ViGEmBus is still
required. The executable is unsigned. The included GitHub Actions workflow also
builds this folder and uploads it as a downloadable artifact when run on GitHub.
Run `python scripts/package_release.py` after building to create the versioned
ZIP and SHA-256 checksum in `releases/`. The GitHub Actions workflow builds on
pushes and pull requests. Pushing a `v*` version tag also publishes a GitHub Release
with the Windows ZIP and checksum. Update `VERSION` before tagging a new version.

## Development and validation

```sh
python -m unittest discover -s tests -v
```

These tests require no hardware or third-party packages. They check button masks,
axis direction/range, analog triggers, deadzone, output clearing, device filtering,
disconnect/reconnect, and failure cleanup with fake devices.

The implementation uses [pygame's SDL controller API](https://www.pygame.org/docs/ref/sdl2_controller.html)
for built-in Stadia USB/Bluetooth mappings and
[vgamepad](https://github.com/yannbouteiller/vgamepad) for virtual output.
Input is polled on Tk's main thread with an 8 ms requested interval; actual latency
depends on Windows scheduling. One controller is supported at a time.

**Verified on the current Windows 11 machine through WSL interop:** SDL detected
Google Stadia Controller over Bluetooth. During a 90-second real-device check,
Windows XInput received 9,016 matching reports with 160 distinct states, including
stick, button, and independent analog trigger input. The Xbox slot disappeared
when the bridge stopped. The Windows executable was compiled locally. This does
not establish behavior in every game or over USB; those remain separate checks.

The ViGEm driver sends a fixed off-center handshake report and suppresses an
unchanged zero report. The bridge primes it with a one-unit stick report and
immediately centers it to avoid startup drift before the first physical input.

For a direct native check with no other bridge instance running:

```powershell
python scripts/verify_windows.py --bridge-seconds 30
```

Move the controller during this check. It compares the live Stadia mapping with
Windows XInput and checks that stopping removes the created Xbox slot.

The optional `scripts/install-local.ps1` and `scripts/build-local.ps1` install a
per-user runtime, build the executable, and create Desktop/Start menu shortcuts.
They require ViGEmBus to be installed separately.
