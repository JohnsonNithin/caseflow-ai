"""Reference dataset for CaseFlow AI clinical information extraction.

All patient identifiers and clinical notes are fictional. No real patient data.

Contract: ClinicalExtractionOutput(patient_id, age, symptoms,
                                   duration_days, oxygen_saturation)

Expected outputs contain only the five fields of the Pydantic output schema.
Use case IDs to report individual errors during evaluation.

Annotation policy:
- Extract only clearly supported facts; use None for absent scalar fields.
- Preserve symptom terminology used by the note (light normalization only).
- Use [] when symptoms are not stated.
- duration_days represents the explicitly stated overall symptom duration.
  If only one symptom has a duration, use that duration. If conflicting
  durations are stated for several symptoms, leave duration_days as None.
- Translate explicit durations: 1 week = 7 days, 48 hours = 2 days,
  yesterday = 1 day, 2 weeks = 14 days. Do not infer duration from dates.
- oxygen_saturation is SpO2 (%), not heart rate or other measurements.
- Ambiguous or contradictory scalar values should be None.
"""

EVALUATION_DATASET = [
    {
        "id": "case_01_basic",
        "input": "Patient P001, age 45, reports fever and dry cough for 3 days. SpO2 is 95%.",
        "expected": {"patient_id": "P001", "age": 45, "symptoms": ["fever", "dry cough"], "duration_days": 3, "oxygen_saturation": 95},
    },
    {
        "id": "case_02_no_id",
        "input": "A 32-year-old patient has headache and nausea for 2 days. Oxygen saturation: 98%.",
        "expected": {"patient_id": None, "age": 32, "symptoms": ["headache", "nausea"], "duration_days": 2, "oxygen_saturation": 98},
    },
    {
        "id": "case_03_no_age",
        "input": "Patient P003 complains of sore throat for 5 days. SpO2 97%.",
        "expected": {"patient_id": "P003", "age": None, "symptoms": ["sore throat"], "duration_days": 5, "oxygen_saturation": 97},
    },
    {
        "id": "case_04_no_duration",
        "input": "Patient P004 (age 61) reports dizziness. Oxygen saturation is 96%. No duration given.",
        "expected": {"patient_id": "P004", "age": 61, "symptoms": ["dizziness"], "duration_days": None, "oxygen_saturation": 96},
    },
    {
        "id": "case_05_no_spo2",
        "input": "Patient P005, 27 years old, has runny nose and sneezing for 4 days. No SpO2 measurement recorded.",
        "expected": {"patient_id": "P005", "age": 27, "symptoms": ["runny nose", "sneezing"], "duration_days": 4, "oxygen_saturation": None},
    },
    {
        "id": "case_06_no_symptoms",
        "input": "Routine checkup: patient P006, aged 50. Denies symptoms. SpO2 99%.",
        "expected": {"patient_id": "P006", "age": 50, "symptoms": [], "duration_days": None, "oxygen_saturation": 99},
    },
    {
        "id": "case_07_hours",
        "input": "P007, 29-year-old, presents with chest tightness for 48 hours; oxygen saturation 94%.",
        "expected": {"patient_id": "P007", "age": 29, "symptoms": ["chest tightness"], "duration_days": 2, "oxygen_saturation": 94},
    },
    {
        "id": "case_08_week",
        "input": "Patient P008 is 40 years old and has had fatigue and muscle aches for one week. SpO2: 97%.",
        "expected": {"patient_id": "P008", "age": 40, "symptoms": ["fatigue", "muscle aches"], "duration_days": 7, "oxygen_saturation": 97},
    },
    {
        "id": "case_09_two_weeks",
        "input": "Record P009: 36-year-old presenting with persistent cough for 2 weeks. SpO2 96%.",
        "expected": {"patient_id": "P009", "age": 36, "symptoms": ["persistent cough"], "duration_days": 14, "oxygen_saturation": 96},
    },
    {
        "id": "case_10_yesterday",
        "input": "Patient P010, age 22, developed abdominal pain yesterday. Oxygen saturation 99%.",
        "expected": {"patient_id": "P010", "age": 22, "symptoms": ["abdominal pain"], "duration_days": 1, "oxygen_saturation": 99},
    },
    {
        "id": "case_11_minimal",
        "input": "Patient reports itching.",
        "expected": {"patient_id": None, "age": None, "symptoms": ["itching"], "duration_days": None, "oxygen_saturation": None},
    },
    {
        "id": "case_12_vitals_not_symptoms",
        "input": "P012, 68-year-old. Blood pressure 130/80 mmHg, pulse 72 bpm, temperature 37.0 C, SpO2 98%. No complaints.",
        "expected": {"patient_id": "P012", "age": 68, "symptoms": [], "duration_days": None, "oxygen_saturation": 98},
    },
    {
        "id": "case_13_negation",
        "input": "Patient P013, 39 years old, has shortness of breath for 2 days but denies fever and cough. SpO2 92%.",
        "expected": {"patient_id": "P013", "age": 39, "symptoms": ["shortness of breath"], "duration_days": 2, "oxygen_saturation": 92},
    },
    {
        "id": "case_14_multiple_symptoms",
        "input": "ID P014; 54 y/o. Fever, chills, headache and body aches over the last 6 days. O2 sat 93%.",
        "expected": {"patient_id": "P014", "age": 54, "symptoms": ["fever", "chills", "headache", "body aches"], "duration_days": 6, "oxygen_saturation": 93},
    },
    {
        "id": "case_15_noise_values",
        "input": "P015; age 47; reports wheezing for 3 days. Heart rate 110 bpm. Temperature 38.2 C. Oxygen saturation 91%.",
        "expected": {"patient_id": "P015", "age": 47, "symptoms": ["wheezing"], "duration_days": 3, "oxygen_saturation": 91},
    },
    {
        "id": "case_16_child",
        "input": "P016 is a 6-year-old child with vomiting and diarrhea for 1 day. SpO2 99%.",
        "expected": {"patient_id": "P016", "age": 6, "symptoms": ["vomiting", "diarrhea"], "duration_days": 1, "oxygen_saturation": 99},
    },
    {
        "id": "case_17_zero_day",
        "input": "Patient P017, age 30, developed a headache today (duration 0 days). SpO2 98%.",
        "expected": {"patient_id": "P017", "age": 30, "symptoms": ["headache"], "duration_days": 0, "oxygen_saturation": 98},
    },
    {
        "id": "case_18_unknown_age",
        "input": "P018; age not documented. Reports nasal congestion for 7 days. O2 saturation 97%.",
        "expected": {"patient_id": "P018", "age": None, "symptoms": ["nasal congestion"], "duration_days": 7, "oxygen_saturation": 97},
    },
    {
        "id": "case_19_conflicting_durations",
        "input": "Patient P019, age 43. Headache for 2 days; cough for 5 days. SpO2 96%. No single overall symptom duration is given.",
        "expected": {"patient_id": "P019", "age": 43, "symptoms": ["headache", "cough"], "duration_days": None, "oxygen_saturation": 96},
    },
    {
        "id": "case_20_missing_oxygen",
        "input": "Patient P020, age 73, has loss of appetite and weakness for 4 days. Pulse oximetry was not performed; pulse rate is 88 bpm.",
        "expected": {"patient_id": "P020", "age": 73, "symptoms": ["loss of appetite", "weakness"], "duration_days": 4, "oxygen_saturation": None},
    },
]

if __name__ == "__main__":
    print(f"Loaded {len(EVALUATION_DATASET)} synthetic evaluation cases")
    for example in EVALUATION_DATASET:
        print(example["id"], "->", example["expected"])
