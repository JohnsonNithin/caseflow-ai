from dotenv import load_dotenv
from langsmith.evaluation import evaluate
from src.llm import ClinicalExtractor

load_dotenv()

extractor = ClinicalExtractor()


# Step 1: Generate predictions
def model_function(inputs):
    result = extractor.extract(inputs["clinical_note"]) # this clinical_note comes from the placeholder in prompt right?
    return result.model_dump()


# Step 2: Algorithmic evaluation
def algorithmic_evaluator(inputs, outputs, reference_outputs):  # and outputs comes from the pydantic output contracts

    age_correct = outputs["age"] == reference_outputs["age"]

    id_correct = outputs["patient_id"] == reference_outputs["patient_id"]

    duration_correct = (outputs["duration_days"] == reference_outputs["duration_days"])

    oxygen_correct = (outputs["oxygen_saturation"] == reference_outputs["oxygen_saturation"])

    # Ignore symptom order and capitalization
    predicted_symptoms = {s.strip().lower() for s in outputs["symptoms"]}
    expected_symptoms = {s.strip().lower() for s in reference_outputs["symptoms"]}
    symptoms_correct = predicted_symptoms == expected_symptoms

    # All five fields must be correct
    overall_correct = all([
        age_correct,
        id_correct,
        duration_correct,
        oxygen_correct,
        symptoms_correct
    ])

    return [
        {"key": "age_accuracy", "score": int(age_correct)},
        {"key": "patient_id_accuracy", "score": int(id_correct)},
        {"key": "duration_accuracy", "score": int(duration_correct)},
        {"key": "oxygen_accuracy", "score": int(oxygen_correct)},
        {"key": "symptoms_accuracy", "score": int(symptoms_correct)},
        {"key": "full_record_accuracy", "score": int(overall_correct)}
    ]


# Step 3: Run LangSmith evaluation
if __name__ == "__main__":
    evaluate(
        model_function,
        data="caseflow-ai-evaluation",
        evaluators=[algorithmic_evaluator],
        experiment_prefix="caseflow-full-extraction-baseline",
        max_concurrency=1
    )