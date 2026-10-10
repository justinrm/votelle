"""Thin commands for offline validation and splitting."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from music_pref.data.ingest import IngestRequest, ingest, prepare_clip
from music_pref.data.manifest import load_config, report_bytes, validate
from music_pref.data.splits import SplitError, write_split
from music_pref.schemas import MusicPrefError, canonical_bytes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="music-pref")
    commands = parser.add_subparsers(dest="command", required=True)
    validate_cmd = commands.add_parser("validate")
    validate_cmd.add_argument("--config", required=True, type=Path)
    split_cmd = commands.add_parser("split")
    split_cmd.add_argument("--config", required=True, type=Path)
    split_cmd.add_argument("--output", required=True, type=Path)
    ingest_cmd = commands.add_parser("ingest")
    ingest_cmd.add_argument("--config", required=True, type=Path)
    ingest_cmd.add_argument("--source-uri", required=True)
    ingest_cmd.add_argument("--raw", required=True, type=Path)
    ingest_cmd.add_argument("--decoded", required=True, type=Path)
    ingest_cmd.add_argument("--acquired-at", required=True)
    ingest_cmd.add_argument("--decode-tool", required=True)
    ingest_cmd.add_argument("--decode-version", required=True)
    ingest_cmd.add_argument("--decode-command", required=True)
    ingest_cmd.add_argument("--rights-record-id")
    ingest_cmd.add_argument("--family-review", type=Path)
    prepare_cmd = commands.add_parser("prepare")
    prepare_cmd.add_argument("--config", required=True, type=Path)
    prepare_cmd.add_argument("--asset-id", required=True)
    prepare_cmd.add_argument("--clip-id", required=True)
    prepare_cmd.add_argument("--start", required=True, type=float)
    prepare_cmd.add_argument("--end", required=True, type=float)
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
    if args.command in {"ingest", "prepare"}:
        try:
            if args.command == "ingest":
                result = ingest(
                    config,
                    IngestRequest(
                        source_uri=args.source_uri,
                        raw_path=args.raw,
                        decoded_path=args.decoded,
                        acquired_at=args.acquired_at,
                        decode_tool=args.decode_tool,
                        decode_version=args.decode_version,
                        decode_command=args.decode_command,
                        rights_record_id=args.rights_record_id,
                        family_review_path=args.family_review,
                    ),
                )
            else:
                result = prepare_clip(config, args.asset_id, args.clip_id, args.start, args.end)
        except MusicPrefError as exc:
            print(json.dumps({"code": exc.code, "remediation": exc.remediation}), file=sys.stderr)
            return 1
        sys.stdout.buffer.write(canonical_bytes(result.model_dump(mode="json")))
        return 0
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
