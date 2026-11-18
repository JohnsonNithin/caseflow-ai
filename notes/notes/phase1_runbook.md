# Phase 01 — Algorithmic Evaluation Runbook

## 1. Objective

Evaluate `ClinicalExtractor` against **20 synthetic clinical notes** with expected answers, and record field-level and full-record accuracy in LangSmith.

## 2. Files and Responsibilities

| File | Purpose |
|---|---|
| `evaluation/dataset.py` | Stores `EVALUATION_DATASET` (20 cases) |
| `evaluation/upload_dataset.py` | Converts and uploads the cases to LangSmith |
| `evaluation/evaluate.py` | Runs the model and scores its predictions |
| `src/llm.py` | Implements `ClinicalExtractor` |

## 3. Prerequisites

- Work from the `caseflow-ai` repository root.
- Use `uv` to run Python.
- `.env` contains the required Groq and LangSmith settings. **Never commit `.env`, API keys, or patient data.**
- LangSmith dataset name: `caseflow-ai-evaluation`.

## 4. Upload or Confirm Reference Cases

```bash
uv run python -m evaluation.upload_dataset
```

**Expected for an existing complete dataset:**

```text
SUCCESS! Your transformation is correct.
Using existing dataset: caseflow-ai-evaluation
Examples in LangSmith: 20
Examples already uploaded. Skipping.
```

The dataset ID is printed by the script. It is an identifier, not an example count.

**Important limitation:** The current skip check skips an upload whenever *any* examples already exist. It does **not** fill partially uploaded datasets. If you see fewer than 20, inspect existing cases and reconcile before uploading; do not blindly rerun or create duplicates.

## 5. Run the Evaluation

```bash
uv run python -m evaluation.evaluate
```

The evaluation runs `ClinicalExtractor` on each note and calculates six metrics: `age_accuracy`, `patient_id_accuracy`, `duration_accuracy`, `oxygen_accuracy`, `symptoms_accuracy`, and `full_record_accuracy`.

The run uses `max_concurrency=1`, meaning one model request at a time.

## 6. Inspect Results in LangSmith

1. Open **Datasets & Experiments**.
2. Select **`caseflow-ai-evaluation`**.
3. Open the latest experiment with prefix **`caseflow-full-extraction-baseline`**.
4. Review the six metrics, then inspect the individual example where `symptoms_accuracy=0`.
5. Check latency, errors, token usage, and cost where available.

## 7. Verified Results — 17 November 2026

| Metric | Accuracy |
|---|---:|
| Age | 100% |
| Patient ID | 100% |
| Duration | 100% |
| Oxygen saturation | 100% |
| Symptoms | 95% |
| Full record | 95% |

This indicates **19/20 fully correct records under current scoring**. The one symptom mismatch has not yet been diagnosed; investigation is deferred to Phase 7.

## 8. Troubleshooting

- **`Examples already uploaded. Skipping.`** — Normal when examples already exist; check the count to confirm completeness.
- **Dataset exists but fewer than 20 examples** — Current upload guard is not a repair mechanism. Compare existing IDs and add missing cases separately.
- **Authentication error** — Check LangSmith and Groq credentials in `.env` and confirm `load_dotenv()` is called.
- **Import error** — Run from the repository root with `uv run python -m evaluation.evaluate`.
- **Rate limits/timeouts** — Keep concurrency at 1 and inspect the failing requests.
- **Unexpected low score** — Open the example in LangSmith and compare prediction to reference; check the scoring rules before changing the prompt.

## 9. Phase Status and Handoff

- **Phase 0 (foundations):** Complete.
- **Phase 1 (algorithmic evaluation baseline):** Complete; full-record accuracy **95%** on 20 synthetic examples.
- **Known follow-up:** Diagnose the symptom mismatch and strengthen tests in Phase 7.
- **Next phase:** Prompt management and versioning. Reuse the same dataset to compare prompt versions.
