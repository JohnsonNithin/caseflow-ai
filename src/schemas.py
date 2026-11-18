
from pydantic import BaseModel, Field, ValidationError, field_validator

class ClinicalNoteInput(BaseModel):
    clinical_note: str = Field(min_length= 1,max_length=5000,description="Clinical note submitted for extraction")

    
    
    @field_validator("clinical_note") # checks the clinical_note field for that we use field validator from pydantic
    @classmethod # its aa class method to access the class itself, self is used to acess the class object
    def validate_clinical_note(cls,value:str) -> str:
        if not value.strip():
            raise ValueError("Invalid input: Clinical note cannot be empty")
        else:
            print("Clinical note validated")
        return value


    
class ClinicalExtractionOutput(BaseModel):
    patient_id: str | None = Field(
        default=None,
        description="Patient identifier explicitly present in the note"
    )
    age: int|None  = Field(default=None, ge=0,le=120, description="Patient age")
    symptoms: list[str] = Field(default_factory=list, description="Patient symptoms")
    duration_days: int| None = Field(default=None, ge=0, description="Patient duration of symptoms")
    oxygen_saturation: int| None = Field(default=None, ge=0, le=100, description="Patient oxygen saturation")





if __name__ == "__main__":

    try:

        CLINICAL_NOTE=""
        result = ClinicalNoteInput(clinical_note=CLINICAL_NOTE)

        print(result.model_dump())
    except ValidationError as e:
        print(e)
