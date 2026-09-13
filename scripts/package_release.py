"""Create a portable Windows release ZIP and SHA-256 checksum."""
import argparse
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dist', type=Path, default=ROOT / 'dist' / 'StadiaBridge')
    parser.add_argument('--output', type=Path, default=ROOT / 'releases')
    args = parser.parse_args()
    version = (ROOT / 'VERSION').read_text().strip()
    if not (args.dist / 'StadiaBridge.exe').is_file() or not (args.dist / '_internal' / 'python312.dll').is_file():
        raise SystemExit('Build the complete Windows app folder before packaging.')
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / f'StadiaBridge-{version}-Windows-x64.zip'
    files = {}
    for path in args.dist.rglob('*'):
        if path.is_file() and path.suffix.lower() not in {'.msi', '.pyc'} and '__pycache__' not in path.parts:
            files[path.relative_to(args.dist)] = path
    for name in ['README.md', 'QUICKSTART.txt', 'LICENSE', 'CHANGELOG.md', 'VERSION']:
        files[Path(name)] = ROOT / name
    for path in (ROOT / 'third_party').rglob('*'):
        if path.is_file():
            files[path.relative_to(ROOT)] = path
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, path in sorted(files.items()):
            archive.write(path, Path('StadiaBridge') / name)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise SystemExit('ZIP integrity check failed.')
    with target.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    (args.output / 'SHA256SUMS.txt').write_text(f'{digest}  {target.name}\n')
    print(f'{target} ({target.stat().st_size:,} bytes; {len(files)} files)')
    print(f'SHA-256: {digest}')


if __name__ == '__main__':
    main()
