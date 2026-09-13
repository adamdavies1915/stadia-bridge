# Windows verification — 2026-09-13

- Host: Windows 11 build 26200, accessed through WSL Windows interop.
- Physical device: Google Stadia Controller, Bluetooth; user confirmed the light
  was on and exercised the controls during verification.
- Existing ViGEmBus service was Running. No new driver was needed.
- A real-controller bridge check received 9,016 matching native XInput reports
  with 160 distinct states over 90 seconds. Observed stick movement, digital
  buttons, and independent analog triggers (including simultaneous LT/RT).
- Stopping that check removed the newly created XInput slot.
- After the startup-centering fix, a separate three-second check received 294
  matching centered reports before any physical movement and removed the slot
  when stopped.
- All 12 mapping/lifecycle tests passed on Windows with Python 3.12.10.
- PyInstaller 6.11.1 successfully built the final Windows executable.
- Final installed executable was launched; its window title
  was `Stadia Bridge`, and Windows reported it Responding.
- Final Plug and Play query reported `Xbox 360 Controller for Windows`, status
  `OK`, device ID `USB\VID_045E&PID_028E\01`.
- An independent process read XInput slot 0 while the packaged app was running,
  including a live left-trigger value of 255. SDL independently listed both
  `Google Stadia Controller` and `Xbox 360 Controller`.
- Desktop and Start menu shortcuts: `Stadia Bridge`.
- Installed executable:
  `%LOCALAPPDATA%\Programs\StadiaBridge\dist\StadiaBridge\StadiaBridge.exe`.

The app was left running. It must remain open (minimized is fine) to keep the
virtual Xbox controller available. USB, rumble, and specific games were not
validated by these checks; rumble forwarding is not implemented.
