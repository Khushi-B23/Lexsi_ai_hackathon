# AyaTrace v2.1 — CuratorKIT source-corpus ingest

## What this file is

`curatorkit_source_corpus.jsonl` is the single CuratorKIT ingest file. It contains **876 records**: exact source text extracted from the AyaTrace multi-source prompt-injection input plan, with AyaTrace identity, pair, source, trust, provenance and track metadata.

This is a **source-corpus ingestion/export** job. It is not the 480-episode runtime dataset, not an SFT/PPO dataset, and not the code that executes Tiny Aya. The full event-level experiment is in the parent AyaTrace v2.1 package (`dataset/event_plan.jsonl`, `episodes.csv`, source objects, spans and chunks).

The YAML explicitly maps JSONL field `text` to CuratorKIT's pretraining `output` field. It uses a schema gate and a corpus exporter, with no generators and no normalizers. This is deliberate: cleaning, Unicode normalization and deduplication could erase the exact attack payloads or collapse matched pairs.

## Confirmed source coverage

| Source type | Records |
|---|---:|
| Documents | 236 |
| Mock tool outputs | 292 |
| Memory objects | 188 |
| Direct user-prompt messages | 160 |
| **Total** | **876** |

The 160 direct-prompt records are messages across 80 episodes (40 matched pairs); they are not 160 attack episodes. The attack/clean conditions and source provenance are retained on every row.

## Install and run

Use Python 3.11 or newer. CuratorKIT 0.1.22 is published on PyPI (released 12 October 2026).

```bash
python -m pip install "curatorkit==0.1.22"
python validate_curatorkit_input.py curatorkit_source_corpus.jsonl
curatorkit run curatorkit_pipeline.yaml --dry-run
curatorkit run curatorkit_pipeline.yaml --output-dir curator_output --verbose
```

On Windows PowerShell, `py -3.11 -m pip install "curatorkit==0.1.22"` can be used instead of the first line.

The dry run checks the pipeline configuration. The full run should then ingest the JSONL, apply the schema gate and write the corpus export and CuratorKIT run metadata. Expected accepted input count is 876; confirm this from CuratorKIT's own run manifest and rejected file.

## Important: do not use this as Aya's conversation runner

CuratorKIT receives the original source objects/messages for curation. It does **not** execute the event plan against Tiny Aya. For the actual experiment, a separate AyaTrace runtime runner must:

1. Read `dataset/event_plan.jsonl` in event order.
2. Reconstruct the accumulated chat history using the exact Tiny Aya chat template.
3. At each `model_generation` event, call Tiny Aya and capture the actual response and token IDs.
4. Append the actual assistant response before executing subsequent events.
5. Execute only sandboxed mock tool and memory operations.
6. Record actual behavioral evaluations and activation tensors in output artifacts.

No failure turn, attack-success label, failing layer/head/neuron, or causal result is prefilled in this source corpus.

## Validation status

- AyaTrace dataset structural validator: **22/22 checks passed** in this build.
- CuratorKIT source JSONL checks: run with the included `validate_curatorkit_input.py`.
- CuratorKIT CLI `--dry-run` and full ingestion: **not executed in this environment**. Run those commands locally and inspect `manifest.json`, `rejected.jsonl`, and `corpus.jsonl` before treating the CuratorKIT stage as complete.
- Tiny Aya tokenizer alignment and inference: **not executed**; these are separate runtime checks.

## Preserve the experiment

Do not turn on `text_cleaner`, Unicode normalization, MinHash/embedding deduplication, or LLM generation for this corpus without a separate experiment-specific justification and preservation test. The raw AyaTrace tables remain authoritative for pair IDs, spans, event chronology and provenance; use the CuratorKIT output as its corpus-ingest artifact.
