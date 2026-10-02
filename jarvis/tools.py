import ast,subprocess,sys,tempfile,uuid
from dataclasses import dataclass
CATASTROPHIC=("fork bomb","mkfs","dd if=","rm -rf /",":(){ :|:& };:")
@dataclass
class ToolResult: ok:bool; output:str; calls:int=0
class PermissionController:
    def __init__(self,mode="smart"): self.mode=mode
    def approve(self,operation):
        low=operation.lower()
        if any(x in low for x in CATASTROPHIC): return False
        if self.mode=="off": return True
        if self.mode=="smart": return operation.split(" ",1)[0] in {"ls","pwd","cat","echo","python","python3"}
        return False
class ToolRegistry:
    def __init__(self): self._tools={}
    def register(self,name,fn): self._tools[name]=fn
    def call(self,name,**kwargs):
        if name not in self._tools: raise KeyError(name)
        return self._tools[name](**kwargs)
class ProgrammaticExecutor:
    def __init__(self,registry,permission,timeout=300,max_calls=50):
        self.registry=registry; self.permission=permission; self.timeout=timeout; self.max_calls=max_calls
    def execute(self,code):
        try: tree=ast.parse(code)
        except SyntaxError as e: return ToolResult(False,f"syntax error: {e}")
        calls=sum(1 for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="tools")
        if calls>self.max_calls: return ToolResult(False,"RPC call limit exceeded",calls)
        if any(x in code.lower() for x in CATASTROPHIC): return ToolResult(False,"catastrophic operation blocked",calls)
        if any(x in code for x in ("os.system(","subprocess.","Popen(")): return ToolResult(False,"direct process execution is blocked",calls)
        path=tempfile.gettempdir()+f"/jarvis_{uuid.uuid4().hex}.py"
        open(path,"w",encoding="utf-8").write(code)
        try:
            p=subprocess.run([sys.executable,path],capture_output=True,text=True,timeout=self.timeout)
            return ToolResult(p.returncode==0,(p.stdout+p.stderr).strip(),calls)
        except subprocess.TimeoutExpired: return ToolResult(False,"execution timeout",calls)
        finally:
            import os; os.unlink(path)
