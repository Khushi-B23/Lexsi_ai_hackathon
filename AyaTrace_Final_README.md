# AyaTrace — Final Research Pack (v1.1)

**Proofread and corrected: 5 November 2026**

Frozen scope: solo project; Tiny Aya Global only initially; document, tool-output and memory injection pathways from the pilot onward; 20 pilot matched pairs, 48 discovery pairs and 24 held-out pairs; attempt a reversible targeted intervention; two Kaggle T4 GPUs.

## Files

- `AyaTrace_Final_Execution_Plan.pdf` — print-friendly master plan.
- `AyaTrace_Final_Execution_Plan.docx` — editable master plan.
- `AyaTrace_Final_Execution_Plan.md` — plain-text/Markdown master plan.
- `AyaTrace_Final_Execution_Notebook.ipynb` — source-aware multi-turn research scaffold, model checks, baseline evaluation, token alignment, activation capture, causal localization, CircuitKIT and release preparation.
- `AyaTrace_Dataset_Schema_v1.0.json` — canonical JSON Schema.

## Frozen dataset allocation

| Split | Retrieved document | Tool output | Memory | Total pairs |
|---|---:|---:|---:|---:|
| Pilot | 7 | 7 | 6 | 20 |
| Discovery | 16 | 16 | 16 | 48 |
| Held out | 8 | 8 | 8 | 24 |
| **Total** | **31** | **31** | **30** | **92** |

Each matched pair contains one clean and one corrupted condition: 184 episode records. `pair_id` joins the pair; `scenario_family_id` is the split-leakage unit.

## Important v1.1 corrections

1. **Provenance is not role.** `attack_source` is distinct from `serialization_role` and `serialization_format`.
2. **All three sources are represented from the pilot.** The initial tool pathway uses a clearly labelled application-generated user envelope. It tests tool-output provenance, not native tool-role semantics. Native tool-role experiments require a verified complete assistant tool-call/result protocol.
3. **Episodes are genuinely multi-turn.** Each starter fixture has at least two assistant decision points after the source is exposed, including a follow-up turn. The fixtures are smoke tests, not the full benchmark.
4. **Memory has write and retrieval events.** The application-side write is not itself a model message; later retrieval is what enters the prompt.
5. **Token spans are run-specific.** Store tokenizer revision, rendered-prompt hash, character span and token span only after prompt/token-ID parity checks. Equal total token length is necessary but not sufficient; verify source-span alignment.
6. **Causal patching uses fixed matched prefixes.** Free-running multi-turn trajectories can diverge; do not patch mismatched positions across unrelated generated histories.
7. **Canary discovery and safety evaluation are separate.** Use a differentiable safe-vs-unsafe continuation objective for circuit discovery. Free generation plus deterministic full/partial leak and simulated-action checks remain behavioral outcomes.
8. **Toolkit APIs are not guessed.** Inspect exact installed versions/signatures and pin commits before wiring CuratorKIT, CircuitKIT and AuditKIT adapters.

## Recommended first run

1. Open the notebook in Kaggle and confirm Python, PyTorch, CUDA and GPU memory.
2. Confirm Hugging Face access and Tiny Aya Global model terms.
3. Load the model on one T4 first. Two T4s do not aggregate their VRAM.
4. Inspect `tokenizer.chat_template`; use an explicit application envelope for tool results in the initial benchmark.
5. Run the offline schema and pair-validation cells before model inference.
6. Complete and manually review the 20-pair pilot across all three sources.
7. Verify that each episode has at least two assistant decision points after source exposure.
8. Run one clean/corrupt pair from each source; verify transcript, canary checker, task-integrity review and multi-turn decision points.
9. Run CircuitKIT's current real-weight Tiny Aya parity tests from the pinned repository revision.
10. Continue to full baseline and mechanistic experiments only after these gates pass.

## Hardware notes

Use one T4 for initial model loading and short-context tests. Keep batch size 1 for activation work. Use the second T4 for a separate independent process only after verifying memory. Do not assume two cards form one 32-GB device. Circuit discovery may need its own model representation; run baseline inference and CircuitKIT in separate sessions if simultaneous memory is a problem.

## Scientific claim boundaries

- Probe separability is not authority understanding.
- Activation differences are correlational.
- EAP-IG is attribution, not proof.
- Patching/ablation provide causal evidence only relative to the tested metric, prompt distribution and controls.
- A circuit is task-, model- and metric-specific.
- The initial tool envelope does not establish native tool-role robustness.
- A successful intervention on synthetic data is not proof of production security. Runtime permissions and tool access controls remain necessary.
- No result is claimed until the user's runtime executes it and the result files are inspected.

## Sources

- Hackathon: https://hackathon.lexsi.ai/
- Tiny Aya Global: https://huggingface.co/CohereLabs/tiny-aya-global
- Tiny Aya technical report: https://arxiv.org/abs/2603.11510
- CircuitKIT: https://github.com/Lexsi-Labs/CircuitKIT
- CircuitKIT custom data: https://circuitkit.lexsi.ai/user-guide/custom-data/
- CircuitKIT evaluation: https://circuitkit.lexsi.ai/user-guide/evaluation/
- CuratorKIT: https://github.com/Lexsi-Labs/CuratorKIT
- AuditKIT: https://github.com/Lexsi-Labs/AuditKIT
- Localization paper: https://arxiv.org/abs/2609.37737
- Prompt Injection as Role Confusion: https://arxiv.org/abs/2603.12277
- CircuitKIT paper: https://arxiv.org/abs/2607.19317

Re-check changing rules, APIs, licenses and model cards at execution time. Pin exact revisions.
