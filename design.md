# CaseFlow AI — System Design

**Version:** 0.1  
**Status:** Phase 1 — Input Validation  
**Domain:** Healthcare Document Intelligence  
**Future Domain:** Insurance Document Processing

## 1. Problem Statement

Healthcare administrative staff manually review clinical documents to identify patient information, symptoms, and other relevant details.

This process can be time-consuming and prone to data-entry errors.

**CaseFlow AI** is an AI-powered document intelligence application that extracts structured information from unstructured clinical notes to support human review.

The architecture will later be adaptable to insurance claims processing.

## 2. Project Objective

Build an end-to-end AI engineering application using Python, LangChain, and Pydantic, progressively integrating RAG, tool calling, AI agents, APIs, databases, evaluation, and production deployment.

The initial version will focus on extracting information from synthetic clinical notes.

## 3. Functional Requirements

**FR-001:** The system shall accept a clinical note as text input.

**FR-002:** The system shall extract explicitly mentioned patient information, including age, symptoms, symptom duration, and oxygen saturation.

**FR-003:** The system shall return extracted information in a predefined JSON structure.

**FR-004:** The system shall not invent values for information missing from the note.

**FR-005:** The system shall reject invalid input before calling the LLM.

**FR-006:** The system shall provide validation errors when input does not satisfy the contract.

## 4. Input Contract

### 4.1 Input Format

The application accepts JSON containing one clinical note.

```json
{
  "clinical_note": "A 52-year-old patient has fever and dry cough for three days. Oxygen saturation is 95%."
}
```

### 4.2 Input Schema

| Field | Type | Required | Constraints |
|---|---|---|---|
| clinical_note | string | Yes | 1–5000 characters; cannot contain only whitespace |

### 4.3 Input Validation Rules

- The `clinical_note` field must be present.
- The input must be a string.
- Empty strings must be rejected.
- Whitespace-only strings must be rejected.
- Strings exceeding 5000 characters must be rejected.
- Invalid inputs must not be sent to the LLM.

## 5. Output Contract

### 5.1 Expected LLM Output

```json
{
  "age": 52,
  "symptoms": [
    "fever",
    "dry cough"
  ],
  "duration_days": 3,
  "oxygen_saturation": 95
}
```

### 5.2 Output Schema

| Field | Type | Missing-value behavior |
|---|---|---|
| age | integer or null | null |
| symptoms | list of strings | Empty list |
| duration_days | integer or null | null |
| oxygen_saturation | integer or null | null |

### 5.3 Output Rules

- Extract only information supported by the original note.
- Do not infer missing medical information.
- Age must be a non-negative integer within the demo's supported range of 0–120.
- Oxygen saturation must be between 0 and 100 when present.
- Duration must be non-negative when expressed in days.
- Output must match the predefined schema.
- Invalid or unsupported output must be handled as a processing failure or flagged for review.

## 6. Error Handling

The application must handle:

- Missing clinical note
- Empty input
- Whitespace-only input
- Invalid input type
- Input exceeding the maximum length
- Invalid LLM output
- LLM provider errors and timeouts

Input validation errors must be handled before calling the LLM.

## 7. Evaluation Criteria

The application will be evaluated for:

- **Extraction accuracy:** How accurately the extracted values match reference answers.
- **Unsupported information:** Whether the LLM invents information not present in the note.
- **Schema validity:** Whether outputs follow the predefined structure.
- **Latency:** How long extraction takes.
- **Cost:** Model API usage per extraction.

Evaluation will use synthetic clinical notes with predefined expected outputs.

## 8. Version 1 Scope

Version 1 includes:

- Text-based clinical note input
- Pydantic input validation
- LangChain LLM integration
- Prompt templates
- Structured information extraction
- Pydantic output validation
- Basic error handling
- Automated tests and evaluation

## 9. Out of Scope — Version 1

- Medical diagnosis
- Treatment recommendations
- Real patient information
- Autonomous clinical decisions
- Insurance claim approval
- RAG, tool calling, and AI agents

These additional engineering capabilities will be introduced in later phases where appropriate.

## 10. Planned Architecture

Clinical Note → Input Validation → Prompt Template → LLM → Output Validation → Structured Result → Evaluation

Future versions will add document ingestion, persistent storage, RAG, tool calling, human review, monitoring, and deployment.

## 11. Definition of Done — Phase 1

- Input contract documented and implemented
- Output contract documented
- Valid and invalid inputs tested
- Whitespace-only input rejected
- Code reviewed
- Changes committed to GitHub
