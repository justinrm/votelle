"""Thin commands for offline validation and splitting."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from music_pref.data.manifest import load_config, report_bytes, validate
from music_pref.data.splits import SplitError, write_split
from music_pref.schemas import canonical_bytes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="music-pref")
    commands = parser.add_subparsers(dest="command", required=True)
    validate_cmd = commands.add_parser("validate")
    validate_cmd.add_argument("--config", required=True, type=Path)
    split_cmd = commands.add_parser("split")
    split_cmd.add_argument("--config", required=True, type=Path)
    split_cmd.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"code": "schema_invalid", "remediation": str(exc)}), file=sys.stderr)
        return 1
    if args.command == "validate":
        report = validate(config)
        sys.stdout.buffer.write(report_bytes(report))
        return 1 if report.has_errors() else 0
    report = validate(config)
    if report.has_errors():
        sys.stderr.buffer.write(report_bytes(report))
        return 1
    try:
        artifact = write_split(config, args.output)
    except SplitError as exc:
        print(json.dumps({"code": exc.code, "remediation": exc.remediation}), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_bytes(artifact))
    return 0


def cli() -> None:
    raise SystemExit(main())
