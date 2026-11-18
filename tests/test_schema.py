
from src.schemas import ClinicalNoteInput, ClinicalExtractionOutput
import pytest
from pydantic import ValidationError






# def test_valid_clinical_note():  # here we are showing using an example- a positive example 

#     note = "Patient has fever."

#     result = ClinicalNoteInput(clinical_note=note)

#     assert result.clinical_note == note # positive example bcs we expect some text as str in note



# def test_empty_note():
#     with pytest.raises(ValidationError): # here we are showing using an example- a negative example 
#                                         #like when its empty string it must raise a validation error.
#         note = "    "

#         ClinicalNoteInput(clinical_note=note)

# @pytest.mark.parametrize(                 
#     "note", ["","  ", "\n\t"]
#     )


#syntax:@pytest.mark.parametrize("variable_name", [value1, value2, value3])



@pytest.mark.parametrize("note", [
    "Patient has fever",
    "Patient has cough"
])
def test_valid_notes(note):
    result = ClinicalNoteInput(clinical_note=note)
    assert result.clinical_note == note # by assert we are tellig that for note varaibel we expect some text as str in note as defined in line 37 of code.


@pytest.mark.parametrize(                 
     "note", ["","  ", "\n\t"]
     )
def test_empty_note(note):
    with pytest.raises(ValidationError):
        ClinicalNoteInput(clinical_note=note)



#@pytest.mark.parametrize("variable_name", [value1, value2, value3])

def test_valid_extraction_output():
    result = ClinicalExtractionOutput(
        patient_id="P001",
        age=52,
        symptoms=["fever", "cough"],
        duration_days=3,
        oxygen_saturation=95
    )
    assert result.age == 52
    assert result.oxygen_saturation == 95