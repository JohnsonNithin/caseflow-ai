# Pattern 02 — Algorithmic Evaluation with LangSmith

## 1. Mental Model

**Reference dataset → Model predictions → Comparison rules → Metric scores → LangSmith experiment**

An evaluation dataset supplies known inputs and expected outputs. The application generates predictions for those inputs. An algorithmic evaluator compares each prediction against the expected answer, and LangSmith records the scores for analysis and comparison.

**Evaluation measures the model; it does not train or fine-tune it.**

## 2. Architecture

| Component | Responsibility | CaseFlow AI |
|---|---|---|
| `evaluation/dataset.py` | Define reference examples | 20 synthetic clinical notes, expected five-field outputs, case IDs |
| `evaluation/upload_dataset.py` | Convert and upload references | `inputs`, `outputs` (reference values), `metadata` |
| `ClinicalExtractor` (`src/llm.py`) | Make predictions | Groq model + Pydantic output |
| `model_function()` (`evaluation/evaluate.py`) | Adapt the application to LangSmith | Accept an `inputs` dictionary; return a prediction dictionary |
| `algorithmic_evaluator()` | Measure correctness | Compare predictions against reference values |
| LangSmith `evaluate()` | Execute and track experiments | Run all examples, collect scores, view individual failures |

## 3. How One Example Works

1. LangSmith provides `inputs = {"clinical_note": "..."}`.
2. `model_function(inputs)` runs `extractor.extract(inputs["clinical_note"])` and returns `result.model_dump()`.
3. The evaluator receives three dictionaries:
   - `inputs`: original clinical note
   - `outputs`: predicted fields
   - `reference_outputs`: expected fields
4. The evaluator returns metric dictionaries such as `{"key": "age_accuracy", "score": 1}`.
5. LangSmith aggregates results across the 20 examples.

**20 examples × 1 model prediction each = 20 model calls per run.** Six scoring checks per example yield up to 120 metric scores; they do not require 120 model calls.

## 4. Metrics in the Current Baseline

- **Age accuracy:** exact match of `age`.
- **Patient ID accuracy:** exact match of `patient_id`.
- **Duration accuracy:** exact match of `duration_days`.
- **Oxygen accuracy:** exact match of `oxygen_saturation`.
- **Symptoms accuracy:** compare sets of symptom strings after trimming whitespace and converting to lowercase; order does not affect the score.
- **Full-record accuracy:** all five field comparisons must be correct for a single note.

Each check produces **1** for a match or **0** otherwise. LangSmith reports aggregate performance across examples.

**Scoring limits:** Both missing scalar values (`None`) count as a match. Symptom matching does not recognize medical synonyms or partial matches; converting symptoms to sets also ignores duplicates. These rules must be reviewed before treating scores as clinical-quality evidence.

## 5. Verified Baseline — 17 November 2026

| Metric | Result |
|---|---:|
| Age accuracy | 100% |
| Patient ID accuracy | 100% |
| Duration accuracy | 100% |
| Oxygen accuracy | 100% |
| Symptoms accuracy | 95% |
| Full-record accuracy | 95% |

**Interpretation:** Under the current strict comparison rules, 19 of 20 synthetic records were completely correct. One example failed the symptom comparison. **That example remains to be investigated in final testing (Phase 7).**

The dataset is a small synthetic benchmark, **not** proof of clinical reliability or readiness for use with patient data.

## 6. Reusable Engineering Principles

- Keep dataset upload separate from evaluation runs.
- Use the **same reference dataset** to compare prompt/model versions fairly.
- Name metrics clearly and version scoring rules when they change.
- Keep expensive model execution separate from cheap, deterministic scoring.
- Use `max_concurrency=1` during debugging or when subject to API rate limits; increase only when justified.
- Track quality alongside latency, errors, token usage, and cost where available.
- Save the failed examples, not only the average score.

## 7. Interview Takeaway

"I built a reference-based evaluation pipeline for a structured LLM extraction system. I uploaded synthetic labeled cases to LangSmith, wrapped the model behind a standard input/output interface, defined deterministic field-level and full-record checks, and tracked a reproducible baseline. I also documented scoring limitations and preserved the same dataset for future prompt comparisons."
