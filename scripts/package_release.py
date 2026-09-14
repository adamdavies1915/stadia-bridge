"""Create a portable Windows release ZIP and SHA-256 checksum."""
import argparse
import hashlib
import shutil
from pathlib import Path
import zipfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dist', type=Path, default=ROOT / 'dist' / 'StadiaBridge')
    parser.add_argument('--single', type=Path, default=ROOT / 'dist' / 'single' / 'StadiaBridge.exe')
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
    for path in (ROOT / 'docs').rglob('*'):
        if path.is_file():
            files[path.relative_to(ROOT)] = path
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
    checksums = [f'{digest}  {target.name}']
    if not args.single.is_file():
        raise SystemExit('Build the single-file executable before packaging.')
    single = args.output / 'StadiaBridge.exe'
    shutil.copy2(args.single, single)
    with single.open('rb') as stream:
        checksums.append(f'{hashlib.file_digest(stream, "sha256").hexdigest()}  {single.name}')
    # Offer the exact LGPL library source alongside its distributed binaries.
    source = args.output / 'pygame-2.6.1.tar.gz'
    source_hash = '56fb02ead529cee00d415c3e007f75e0780c655909aaa8e8bf616ee09c9feb1f'
    if not source.is_file():
        url = 'https://files.pythonhosted.org/packages/49/cc/08bba60f00541f62aaa252ce0cfbd60aebd04616c0b9574f755b583e45ae/pygame-2.6.1.tar.gz'
        with urlopen(url, timeout=60) as response:
            source.write_bytes(response.read())
    with source.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != source_hash:
            raise SystemExit('pygame source checksum mismatch.')
    checksums.append(f'{source_hash}  {source.name}')
    (args.output / 'SHA256SUMS.txt').write_text('\n'.join(checksums) + '\n')
    print(f'{target} ({target.stat().st_size:,} bytes; {len(files)} files)')
    print(f'SHA-256: {digest}')


if __name__ == '__main__':
    main()
