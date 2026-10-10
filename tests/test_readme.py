from pathlib import Path


def test_readme_does_not_treat_fixtures_as_preference_evidence():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "Fixture success is not evidence of preference prediction." in text
