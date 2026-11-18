from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from src.schemas import ClinicalNoteInput, ClinicalExtractionOutput
from src.prompt import prompt
print(load_dotenv())


model="openai/gpt-oss-20b"
model_provider="groq"
temperature=0.5


class ClinicalExtractor:
    def __init__(self):
        self.model = init_chat_model(model=model,model_provider=model_provider,temperature=temperature)
        self.prompt = prompt
        self.structured_model = self.model.with_structured_output(ClinicalExtractionOutput)

    def extract(self, any_user_note: str) -> ClinicalExtractionOutput:

        #step1: validate the input and raise an error if it's invalid
        InputValidation = ClinicalNoteInput(clinical_note=any_user_note) # clinical_note is the place holder inside the prompt and any_user_note is the incoming note from user

        #step2 :format the prompt
        prompt_formatting = self.prompt.format(clinical_note=InputValidation.clinical_note) 
        # InputValidation is the pydantic objecct and for accessing its attribute which is clinical_note we use InputValidation.clinical_note  

        # step 3: call LLM with structured output
        result = self.structured_model.invoke(prompt_formatting)

        # Step 4:returning result
        return result


if __name__ == "__main__":
    result = ClinicalExtractor().extract(any_user_note="Patient has fever and dry cough for three days. Oxygen saturation is 95%.")
    print(result)
    












