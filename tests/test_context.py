from jarvis.context import ContextManager
from jarvis.state import StateStore

def test_compression_threshold(tmp_path):
    store=StateStore(str(tmp_path/"state.db"))
    cm=ContextManager(store, max_tokens=100, threshold=.5, target_ratio=.2, protect_last_n=2)
    messages=[{"role":"user","content":"x"*500} for _ in range(3)]
    assert cm.needs_compression(messages)
