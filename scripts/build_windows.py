"""Build portable-folder and single-file Windows apps without bundling a driver."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    if sys.platform != 'win32':
        raise SystemExit('Build this application on Windows.')
    import PyInstaller.__main__
    from importlib.util import find_spec
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', choices=['folder', 'single', 'both'], default='both')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--work', type=Path, default=ROOT / 'build')
    args = parser.parse_args()
    spec = find_spec('vgamepad')
    if spec is None or not spec.submodule_search_locations:
        raise SystemExit('Run setup.bat first.')
    package = Path(next(iter(spec.submodule_search_locations)))
    dll = package / 'win/vigem/client/x64/ViGEmClient.dll'
    if not dll.is_file():
        raise SystemExit('The Windows x64 ViGEmClient library is missing.')
    common = [
        '--noconfirm', '--clean', '--windowed', '--name', 'StadiaBridge',
        '--hidden-import', 'pygame._sdl2.controller',
        '--add-binary', f'{dll};vgamepad/win/vigem/client/x64',
        '--add-data', f'{ROOT / "third_party"};third_party',
        '--add-data', f'{ROOT / "LICENSE"};.',
    ]
    for mode in (['folder', 'single'] if args.format == 'both' else [args.format]):
        output = args.output / 'single' if mode == 'single' else args.output
        work = args.work / mode
        work.mkdir(parents=True, exist_ok=True)
        PyInstaller.__main__.run(common + [
            '--onefile' if mode == 'single' else '--onedir',
            '--distpath', str(output), '--workpath', str(work), '--specpath', str(work),
            str(ROOT / 'run.py'),
        ])


if __name__ == '__main__':
    main()
