#!/usr/bin/env python3
"""Validate the AyaTrace v2.1 CuratorKIT JSONL before ingestion."""
import argparse, collections, hashlib, json, sys
from pathlib import Path

EXPECTED_TOTAL = 876
EXPECTED_SOURCE_COUNTS = {
    "document": 236,
    "tool": 292,
    "memory": 188,
    "direct_prompt": 160,
}
REQUIRED = {
    "id", "text", "source_file", "source_uri", "row_id", "track",
    "record_type", "world_entity_id", "parent_row_id", "content_hash",
    "schema_version", "episode_id", "pair_id", "dataset_split", "condition",
    "source_id", "source_type", "origin_role", "trust_label"
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", nargs="?", default="curatorkit_source_corpus.jsonl")
    args = ap.parse_args()
    path = Path(args.jsonl)
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors = []
    if len(rows) != EXPECTED_TOTAL:
        errors.append(f"expected {EXPECTED_TOTAL} records, found {len(rows)}")
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate id values")
    row_ids = [r.get("row_id") for r in rows]
    if len(row_ids) != len(set(row_ids)):
        errors.append("duplicate row_id values")
    src_counts = collections.Counter(r.get("source_type") for r in rows)
    if dict(src_counts) != EXPECTED_SOURCE_COUNTS:
        errors.append(f"source counts mismatch: {dict(src_counts)}")
    for idx, r in enumerate(rows, 1):
        missing = REQUIRED - set(r)
        if missing:
            errors.append(f"line {idx}: missing fields {sorted(missing)}")
        text = r.get("text", "")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"line {idx}: empty/non-string text")
            continue
        actual = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
        if r.get("content_hash") != actual:
            errors.append(f"line {idx}: content_hash does not match exact UTF-8 text")
        if r.get("source_type") == "direct_prompt":
            if r.get("origin_role") != "user":
                errors.append(f"line {idx}: direct_prompt source origin_role is not user")
            if r.get("instruction_priority") != "user_level_below_system":
                errors.append(f"line {idx}: direct_prompt priority label is unexpected")
    print(json.dumps({
        "file": str(path),
        "records": len(rows),
        "source_counts": dict(src_counts),
        "attack_content_records": sum(bool(r.get("is_attack_content")) for r in rows),
        "errors": errors,
        "passed": not errors
    }, indent=2, ensure_ascii=False))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
