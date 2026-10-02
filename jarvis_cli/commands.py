from __future__ import annotations
import argparse,sys
APP="jarvis"
TOP=["chat","model","moa","fallback","gateway","proxy","egress","lsp","setup","whatsapp","whatsapp-cloud","slack","auth","login","logout","send","prompt-size","config","completion","profile","tools","skills","doctor","update","acp"]
SLASH=["help","new","reset","model","personality","retry","undo","compress","usage","insights","skills","stop","platforms","status","sethome","save","quit","exit","profile","tools","gateway","login","logout","update","subscription","image","paste","copy","debug"]
def main(argv=None):
    p=argparse.ArgumentParser(prog=APP,description="JARVIS Agent — a rebranded Hermes-compatible agent runtime")
    p.add_argument("--version","-V",action="version",version=f"JARVIS Agent {__import__('jarvis_cli').__version__}")
    p.add_argument("--profile","-p"); p.add_argument("--resume","-r"); p.add_argument("--continue","-c",dest="cont",nargs="?")
    p.add_argument("--in",dest="workdir"); p.add_argument("--worktree","-w",action="store_true")
    p.add_argument("--yolo",action="store_true"); p.add_argument("--pass-session-id",action="store_true")
    p.add_argument("--ignore-user-config",action="store_true"); p.add_argument("--ignore-rules",action="store_true")
    p.add_argument("--tui",action="store_true"); p.add_argument("--cli",action="store_true"); p.add_argument("--dev",action="store_true")
    sub=p.add_subparsers(dest="command")
    chat=sub.add_parser("chat"); chat.add_argument("-q","--query"); chat.add_argument("--model"); chat.add_argument("--provider"); chat.add_argument("--toolsets"); chat.add_argument("-s","--skill",action="append"); chat.add_argument("--verbose",action="store_true")
    for name in TOP:
        if name!="chat": sub.add_parser(name)
    sub.add_parser("help")
    ns,rest=p.parse_known_args(argv)
    if ns.command is None:
        return interactive()
    if ns.command=="help":
        print("JARVIS commands:\n  "+"\n  ".join(TOP)); print("\nSlash commands:\n  /"+"\n  /".join(SLASH)); return
    if ns.command=="chat":
        prompt=ns.query
        if prompt: print("[JARVIS] "+prompt); return
        return interactive()
    print(f"[JARVIS] {ns.command}: command interface registered. Runtime adapter pending.")
def interactive():
    print("╭─ JARVIS ─────────────────────────────────────────╮")
    print("│ JARVIS Agent                                     │")
    print("│ Type /help for commands. /quit exits.            │")
    print("╰──────────────────────────────────────────────────╯")
    while True:
        try: text=input("❯ ")
        except (EOFError,KeyboardInterrupt): print(); return
        if text.strip() in {"/quit","/exit"}: return
        if text.strip()=="/help": print("Commands: "+" ".join("/"+x for x in SLASH)); continue
        if text.strip(): print("[JARVIS] "+text)
