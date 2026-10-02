from jarvis.state import StateStore
def test_fts_roundtrip(tmp_path):
    s=StateStore(str(tmp_path/"state.db")); s.upsert_session("s","default","mock")
    s.add_message("s","user","deploy the JARVIS gateway",5)
    rows=s.search_messages("JARVIS")
    assert rows and "gateway" in rows[0]["content"]
