from votelle_music.cli import main
from tests.fixtures.build import build_dataset, write_config


def test_cli_validate_and_split_exit_codes(tmp_path):
    ok = build_dataset(tmp_path / "ok", families=1)
    assert main(["validate", "--config", str(write_config(tmp_path / "ok.json", ok))]) == 0

    bad = build_dataset(tmp_path / "bad", families=1, rights_mode="omit")
    assert main(["validate", "--config", str(write_config(tmp_path / "bad.json", bad))]) == 1

    chain = build_dataset(tmp_path / "chain", families=4, link="chain")
    output = tmp_path / "no.json"
    assert main(["split", "--config", str(write_config(tmp_path / "chain.json", chain)), "--output", str(output)]) == 1
    assert not output.exists()


def test_cli_split_writes_a_stable_artifact(tmp_path):
    root = build_dataset(tmp_path / "data", families=20)
    output = tmp_path / "runs" / "split.json"
    code = main(["split", "--config", str(write_config(tmp_path / "config.json", root)), "--output", str(output)])
    assert code == 0
    assert output.is_file()
