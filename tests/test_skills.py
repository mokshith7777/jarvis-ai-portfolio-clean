from jarvis.skills import SkillStore

def test_skill_limits(tmp_path):
    s=SkillStore(str(tmp_path))
    name=s.save("deploy-check","check deployment","1. inspect logs\n2. verify health")
    assert name=="deploy-check"
    assert "deploy-check.md" in s.list()
