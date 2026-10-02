#!/usr/bin/env python3
"""Materialize the upstream Hermes Agent implementation as a JARVIS-branded derivative."""
from pathlib import Path
import shutil, subprocess, tempfile
ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "https://github.com/NousResearch/hermes-agent.git"
JARVIS_REPO = "https://github.com/mokshith7777/jarvis-ai-portfolio-clean"
SKIP_ROOT = {".git", ".github", ".jarvis", "node_modules", ".venv"}
PATH_REPLACEMENTS = (
    ("hermes-agent", "jarvis-agent"), ("hermes_cli", "jarvis_cli"),
    ("HERMES_HOME", "JARVIS_HOME"), ("HERMES_TUI", "JARVIS_TUI"),
    ("HERMES_", "JARVIS_"), (".hermes", ".jarvis"),
    ("HERMES", "JARVIS"), ("Hermes", "JARVIS"), ("hermes", "jarvis"),
)
TEXT_REPLACEMENTS = PATH_REPLACEMENTS + (
    ("https://hermes-agent.nousresearch.com", JARVIS_REPO),
    ("https://github.com/NousResearch/hermes-agent", JARVIS_REPO),
)
BINARY_EXTENSIONS = {".png",".jpg",".jpeg",".gif",".webp",".ico",".woff",".woff2",".ttf",".otf",".zip",".gz",".xz",".7z",".db",".sqlite",".so",".dylib",".dll",".exe",".bin",".node"}
def clone_upstream():
    tmp = Path(tempfile.mkdtemp(prefix="jarvis-upstream-"))
    subprocess.run(["git","clone","--depth","1","--recurse-submodules",UPSTREAM,str(tmp)], check=True)
    return tmp
def copy_upstream(src):
    # Remove the pre-parity JARVIS scaffold first. Otherwise a renamed upstream
    # directory such as hermes -> jarvis can collide with the old scaffold.
    for legacy in ["jarvis", "jarvis_cli", "gateway", "tools", "tests", "skills", "plugins", "run_agent.py", "model_tools.py", "toolsets.py", "hermes_state.py", "pyproject.toml", "README.md"]:
        target = ROOT / legacy
        if target.is_dir(): shutil.rmtree(target)
        elif target.exists(): target.unlink()
    for item in src.iterdir():
        if item.name in {".git",".github"}: continue
        dest = ROOT / item.name
        if dest.is_dir() and item.is_dir(): shutil.rmtree(dest)
        elif dest.exists(): dest.unlink()
        if item.is_dir(): shutil.copytree(item,dest)
        else: shutil.copy2(item,dest)
def rename_paths():
    candidates=[p for p in ROOT.rglob("*") if not any(part in SKIP_ROOT for part in p.parts) and p.name not in {"UPSTREAM_NOTICE.md","JARVIS_BRANDING.md"}]
    for path in sorted(candidates,key=lambda p:len(p.parts),reverse=True):
        name=path.name
        for old,new in PATH_REPLACEMENTS: name=name.replace(old,new)
        if name != path.name: path.rename(path.with_name(name))
def transform_text():
    for path in ROOT.rglob("*"):
        if (not path.is_file() or any(part in SKIP_ROOT for part in path.parts) or path.name in {"UPSTREAM_NOTICE.md","JARVIS_BRANDING.md","LICENSE"} or path.suffix.lower() in BINARY_EXTENSIONS): continue
        try:
            raw=path.read_bytes()
            if b"\x00" in raw[:8192]: continue
            text=raw.decode("utf-8")
        except (OSError,UnicodeDecodeError): continue
        out=text
        for old,new in TEXT_REPLACEMENTS: out=out.replace(old,new)
        if out != text: path.write_text(out,encoding="utf-8")
def validate_tree():
    required=["pyproject.toml","jarvis_cli","run_agent.py","jarvis_state.py","tools/registry.py","gateway/run.py","skills","tests"]
    missing=[x for x in required if not (ROOT/x).exists()]
    if missing: raise SystemExit("Missing after JARVIS migration: "+", ".join(missing))
    py=(ROOT/"pyproject.toml").read_text(encoding="utf-8")
    if 'name = "jarvis-agent"' not in py: raise SystemExit("pyproject package name was not rebranded")
    if "jarvis_cli.main:main" not in py: raise SystemExit("jarvis CLI entrypoint was not found")
    bad=[]
    for root in ["jarvis_cli","agent","gateway","tools","plugins","run_agent.py","model_tools.py"]:
        target=ROOT/root
        if not target.exists(): continue
        files=[target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]
        for p in files:
            try: body=p.read_text(encoding="utf-8",errors="ignore")
            except OSError: continue
            if "hermes_cli" in body or "HERMES_HOME" in body or "HERMES_TUI" in body: bad.append(str(p.relative_to(ROOT)))
    if bad: raise SystemExit("Legacy runtime identifiers remain: "+", ".join(bad[:20]))
def write_branding_manifest():
    (ROOT/"JARVIS_BRANDING.md").write_text("# JARVIS branding\n\nJARVIS is a separately branded derivative implementation of the open-source Hermes Agent codebase. The full source is materialized here, so JARVIS has no runtime dependency on an external Hermes checkout.\n\nRuntime identity: jarvis CLI, .jarvis configuration, JARVIS_HOME environment, JARVIS gateway/service, JARVIS API, JARVIS skills/tools/providers.\n\nUpstream: Nous Research Hermes Agent, MIT licensed. See UPSTREAM_NOTICE.md and LICENSE.\n",encoding="utf-8")
def main():
    upstream=clone_upstream()
    copy_upstream(upstream)
    rename_paths()
    transform_text()
    write_branding_manifest()
    validate_tree()
    print("JARVIS source parity tree generated and validated.")
if __name__=="__main__": main()