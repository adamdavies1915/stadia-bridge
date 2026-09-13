"""Install vgamepad without launching its obsolete bundled driver installer."""
import hashlib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from urllib.request import urlopen

URL = 'https://files.pythonhosted.org/packages/8a/54/0eaddc33f84247963af078f364b37153d09fcd6cdc398f243ec3e8842c56/vgamepad-0.1.0.tar.gz'
SHA256 = '57f6bd01aec0c172947517fb782d150ef9b285f7f4d524c317374fa5c24a89de'


def main():
    root = Path(__file__).resolve().parent
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(root / 'requirements.txt')], check=True)
    if sys.platform != 'win32':
        return
    try:
        if version('vgamepad') == '0.1.0':
            return
    except PackageNotFoundError:
        pass
    with tempfile.TemporaryDirectory(prefix='stadia-vgamepad-') as temp:
        folder = Path(temp)
        with urlopen(URL, timeout=60) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != SHA256:
            raise RuntimeError('vgamepad archive checksum mismatch')
        archive = folder / 'vgamepad.tar.gz'
        archive.write_bytes(data)
        with tarfile.open(archive) as package:
            package.extractall(folder, filter='data')
        source = folder / 'vgamepad-0.1.0'
        setup = source / 'setup.py'
        content = setup.read_text(encoding='utf-8')
        guard = 'if not vigem_installed:'
        if content.count(guard) != 1:
            raise RuntimeError('Unexpected vgamepad installer structure')
        # Runtime and DLLs are unchanged. Only the MSI auto-launch is disabled.
        setup.write_text(content.replace(guard, 'if False:  # Driver installed separately by the user.'), encoding='utf-8')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-deps', str(source)], check=True)


if __name__ == '__main__':
    main()
