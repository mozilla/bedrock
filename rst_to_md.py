import os
import subprocess
from pathlib import Path

IN_DIR = Path("docs")
OUT_DIR = Path("mkdocs")
rst_files = IN_DIR.rglob("*.rst")

for fpath in rst_files:
    fpath = fpath.relative_to(IN_DIR)
    in_file = f"{IN_DIR}/{fpath}"
    out_file = f"{OUT_DIR}/{fpath.with_suffix('.md')}"
    cmd = f"pandoc -s -f rst -t markdown -o {out_file} {in_file}"
    print(cmd)
    subprocess.run(cmd, shell=True)
