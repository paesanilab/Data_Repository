"""Run all four independent numerical reproducer scripts in this folder."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if __name__ == '__main__':
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for figure in (1, 2, 3, 4):
        subprocess.run([sys.executable, str(ROOT / f'reproduce_figure_{figure}.py')],
                       cwd=ROOT, env=env, check=True)
    print('Reproduced 19 numerical panel PNGs from local TSVs only.')
