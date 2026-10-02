from jarvis.context import ContextManager
from jarvis.state import StateStore
def test_compression_threshold(tmp_path):
    s=StateStore(str(tmp_path/"state.db")); cm=ContextManager(s,100,.5,.2,2)
    msgs=[{"role":"user","content":"x"*500} for _ in range(3)]
    assert cm.needs_compression(msgs)
