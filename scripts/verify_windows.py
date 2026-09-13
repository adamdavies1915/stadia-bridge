"""Read Windows XInput directly; optionally exercise the real Stadia bridge."""
import argparse
import ctypes
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stadia_bridge.bridge import SDLSource, Bridge, xbox_factory


class Gamepad(ctypes.Structure):
    _fields_ = [('buttons', ctypes.c_uint16), ('lt', ctypes.c_uint8),
                ('rt', ctypes.c_uint8), ('lx', ctypes.c_int16),
                ('ly', ctypes.c_int16), ('rx', ctypes.c_int16), ('ry', ctypes.c_int16)]


class State(ctypes.Structure):
    _fields_ = [('packet', ctypes.c_uint32), ('gamepad', Gamepad)]


def xinput_states():
    api = ctypes.WinDLL('xinput1_4.dll')
    api.XInputEnable.argtypes = [ctypes.c_int]
    api.XInputEnable(1)
    api.XInputGetState.argtypes = [ctypes.c_uint32, ctypes.POINTER(State)]
    api.XInputGetState.restype = ctypes.c_uint32
    states = {}
    for index in range(4):
        state = State()
        if api.XInputGetState(index, ctypes.byref(state)) == 0:
            states[index] = {name: getattr(state.gamepad, name) for name, _ in Gamepad._fields_}
    return states


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bridge-seconds', type=float, default=0)
    args = parser.parse_args()
    baseline = xinput_states()
    print(json.dumps({'xinput_before': baseline}), flush=True)
    source = SDLSource()
    bridge = Bridge(source, xbox_factory)
    try:
        source.pump()
        print(json.dumps({'sdl_version': source.pygame.get_sdl_version(), 'devices': source.names()}), flush=True)
        for index, name in source.names():
            if 'stadia' in name.casefold():
                c = source.open(index)
                print(json.dumps({'name': name, 'mapping': c.get_mapping(), 'axes': [c.get_axis(i) for i in range(6)]}), flush=True)
                c.quit()
        if args.bridge_seconds:
            bridge.start()
            deadline = time.monotonic() + args.bridge_seconds
            matched = 0
            observed = set()
            slots = set()
            last_print = 0
            while time.monotonic() < deadline:
                bridge.tick()
                if not bridge.enabled:
                    raise RuntimeError(bridge.status)
                states = xinput_states()
                # Guide is not exposed through the documented XInputGetState API.
                expected = dict(vars(bridge.report))
                expected['buttons'] &= ~0x400
                for index in states.keys() - baseline.keys():
                    slots.add(index)
                    if states[index] == expected and bridge.pad is not None:
                        matched += 1
                        observed.add(tuple(states[index].values()))
                now = time.monotonic()
                if now - last_print >= 2:
                    print(json.dumps({'status': bridge.status, 'xinput': states, 'expected': expected}), flush=True)
                    last_print = now
                time.sleep(.008)
            print(json.dumps({'matched_native_reports': matched, 'distinct_reports': len(observed), 'created_xinput_slots': sorted(slots)}), flush=True)
            if not matched:
                raise RuntimeError('No native XInput reports matched the connected Stadia controller')
    finally:
        bridge.stop()
        source.close()
    if args.bridge_seconds:
        time.sleep(.5)
        after = xinput_states()
        print(json.dumps({'xinput_after_stop': after}), flush=True)
        if set(after) - set(baseline):
            raise RuntimeError('Created Xbox controller still present after Stop')


if __name__ == '__main__':
    main()
