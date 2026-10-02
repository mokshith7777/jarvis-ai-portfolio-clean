from __future__ import annotations
import ast, json, os, subprocess, sys, tempfile, uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

CATASTROPHIC = ("fork bomb", "mkfs", "dd if=", "rm -rf /", ":(){ :|:& };:")

@dataclass
class ToolResult:
    ok: bool
    output: str
    calls: int = 0

class PermissionController:
    def __init__(self, mode="smart"): self.mode=mode

    def approve(self, operation: str) -> bool:
        low=operation.lower()
        if any(x in low for x in CATASTROPHIC): return False
        if self.mode=="off": return True
        if self.mode=="smart":
            return operation.split(" ",1)[0] in {"ls","pwd","cat","echo","python","python3"}
        return False

class ToolRegistry:
    def __init__(self): self._tools: dict[str,Callable]= {}
    def register(self,name,fn): self._tools[name]=fn
    def call(self,name,**kwargs):
        if name not in self._tools: raise KeyError(name)
        return self._tools[name](**kwargs)

class ProgrammaticExecutor:
    def __init__(self, registry: ToolRegistry, permission: PermissionController,
                 timeout=300, max_calls=50):
        self.registry=registry; self.permission=permission
        self.timeout=timeout; self.max_calls=max_calls

    def execute(self, code: str) -> ToolResult:
        try: ast.parse(code)
        except SyntaxError as e: return ToolResult(False,f"syntax error: {e}")
        calls=0
        events=[]
        for node in ast.walk(ast.parse(code)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id=="tools":
                    calls += 1
        if calls > self.max_calls: return ToolResult(False,"RPC call limit exceeded",calls)
        for line in code.splitlines():
            stripped=line.strip()
            if stripped.startswith(("os.system(","subprocess.","Popen(")):
                return ToolResult(False,"direct process execution is blocked")
        # The local fallback only exposes the registered tool bridge.
        bridge_path=Path(tempfile.gettempdir())/f"jarvis_{uuid.uuid4().hex}.py"
        safe = "from jarvis.tools import ToolBridge\n"
        safe += "tools=ToolBridge()\n"
        safe += code
        bridge_path.write_text(safe, encoding="utf-8")
        try:
            p=subprocess.run([sys.executable,str(bridge_path)],capture_output=True,
                             text=True,timeout=self.timeout,env={"PATH":os.environ.get("PATH","")})
            out=(p.stdout+p.stderr).strip()
            return ToolResult(p.returncode==0,out,calls)
        except subprocess.TimeoutExpired:
            return ToolResult(False,"execution timeout",calls)
        finally:
            bridge_path.unlink(missing_ok=True)

class ToolBridge:
    # Child-process bridge is intentionally minimal. Production deployments should
    # replace this with a Unix-domain-socket RPC broker backed by ToolRegistry.
    def __getattr__(self,name):
        raise RuntimeError("ToolBridge is not connected in the standalone worker")
