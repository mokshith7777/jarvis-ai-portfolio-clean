#!/usr/bin/env python3
"""Build a JARVIS-branded derivative from the upstream MIT Hermes Agent tree.

The upstream project remains the behavioral reference. This script deliberately
preserves LICENSE/UPSTREAM_NOTICE.md and transforms product-facing identifiers:
hermes-agent -> jarvis-agent, hermes_cli -> jarvis_cli, HERMES -> JARVIS,
Hermes -> JARVIS, hermes -> jarvis, .hermes -> .jarvis.
"""
from pathlib import Path
import shutil, subprocess, tempfile

ROOT=Path(__file__).resolve().parents[1]
UPSTREAM="https://github.com/NousResearch/hermes-agent.git"
KEEP={"UPSTREAM_NOTICE.md","LICENSE",".git",".github"}

def clone():
    tmp=Path(tempfile.mkdtemp(prefix="jarvis-upstream-"))
    subprocess.run(["git","clone","--depth","1",UPSTREAM,str(tmp)],check=True)
    return tmp

def copy_tree(src):
    for item in src.iterdir():
        if item.name in {".git",".github"}: continue
        dest=ROOT/item.name
        if dest.is_dir(): shutil.rmtree(dest)
        elif dest.exists(): dest.unlink()
        if item.is_dir(): shutil.copytree(item,dest)
        else: shutil.copy2(item,dest)

def rename_paths():
    paths=sorted([p for p in ROOT.rglob("*") if p.name not in KEEP], key=lambda p: len(p.parts), reverse=True)
    for p in paths:
        new_name=p.name.replace("hermes-agent","jarvis-agent").replace("hermes_cli","jarvis_cli").replace("HERMES","JARVIS").replace("Hermes","JARVIS").replace("hermes","jarvis")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

def transform_text():
    binary_ext={".png",".jpg",".jpeg",".gif",".webp",".ico",".woff",".woff2",".ttf",".otf",".zip",".gz",".db"}
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(part in {".git",".venv","node_modules"} for part in p.parts): continue
        if p.suffix.lower() in binary_ext: continue
        try: raw=p.read_bytes()
        except OSError: continue
        if b"\x00" in raw[:4096]: continue
        try: text=raw.decode("utf-8")
        except UnicodeDecodeError: continue
        out=(text.replace("hermes-agent","jarvis-agent")
                  .replace("hermes_cli","jarvis_cli")
                  .replace("HERMES","JARVIS")
                  .replace("Hermes","JARVIS")
                  .replace("hermes","jarvis")
                  .replace(".jarvis-agent","/jarvis-agent"))
        if out != text: p.write_text(out,encoding="utf-8")

def main():
    upstream=clone()
    copy_tree(upstream)
    rename_paths()
    transform_text()
    print("JARVIS upstream parity tree generated from",UPSTREAM)

if __name__=="__main__": main()
