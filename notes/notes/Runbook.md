
# CaseFlow AI — Developer Runbook

## 1. Project Setup

Install dependencies:

```bash
uv sync
```

## 2. Environment Configuration

Create a local `.env` file containing:

- GROQ_API_KEY
- LANGSMITH_API_KEY
- LANGSMITH_TRACING=true
- LANGSMITH_PROJECT=caseflow-ai

Never commit `.env` to GitHub.

## 3. Run Clinical Extraction

```bash
uv run python -m src.llm
```

Execution flow:

1. Load environment variables.
2. Initialize ClinicalExtractor.
3. Validate the clinical note.
4. Format the prompt.
5. Invoke Groq with structured output.
6. Return extracted patient information.

## 4. Run Schema Tests

```bash
uv run pytest
```

## 5. Evaluation Workflow

1. Prepare the reference dataset.
1.1 create api key for langsmith and then save it .env and then run the extractor which is llm.pys so that you can see the projects name in Langsmith UI>Tracing .
2. Upload examples to LangSmith 
3. Run the evaluation experiment.
4. Review accuracy, latency, and failures.
5. Compare experiments after changing the prompt or model.

## 6. Troubleshooting

Document recurring errors here:

- Error message
- Root cause
- Solution

## 7. Useful Commands

| Command | Purpose |
|---|---|
| `uv sync` | Recreate project environment |
| `uv add package_name` | Install and record a dependency |
| `uv run python -m src.llm` | Run the extractor |
| `uv run pytest` | Run Python tests |
| `git status` | Inspect changed files |
