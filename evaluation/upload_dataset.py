from evaluation.dataset import EVALUATION_DATASET
from langsmith import Client
from dotenv import load_dotenv





#print(load_dotenv())
load_dotenv()


# Create a LangSmith client
ls_client = Client()
examples_data = []

# WRITE YOUR SOLUTION HERE

for example in EVALUATION_DATASET:
    converted_example = {
        "inputs": {
            "clinical_note": example["input"] 
        },
        "outputs": example["expected"],
        "metadata": {
            "case_id": example["id"]
        }
    }

    examples_data.append(converted_example)


def create_dataset(dataset_name, description=""):
    if ls_client.has_dataset(dataset_name=dataset_name):
        dataset = ls_client.read_dataset(dataset_name=dataset_name)
        print(f"Using existing dataset: {dataset_name}")
    else:
        dataset = ls_client.create_dataset(
            dataset_name=dataset_name,
            description=description
        )
        print(f"Created new dataset: {dataset_name}")

    return dataset


def add_examples_to_dataset(dataset_id, examples_data):
    ls_client.create_examples(dataset_id = dataset_id,
                           examples = examples_data)
    print(f"Added {len(examples_data)} examples to dataset")





if __name__ == "__main__":
   

    assert len(examples_data) == 20, "Incorrect transformation. Review your code."
    print("\nSUCCESS! Your transformation is correct.")



    dataset=create_dataset(dataset_name = "caseflow-ai-evaluation", description = "CaseFlow AI evaluation dataset")
    print(dataset.id)
    existing_examples = list(ls_client.list_examples(dataset_id=dataset.id)) # convertingto list to check the length of the list.
    print("Examples in LangSmith:", len(existing_examples))

    if not any(ls_client.list_examples(dataset_id=dataset.id)):
        add_examples_to_dataset(dataset.id, examples_data)
    else:
        print("Examples already uploaded. Skipping.")


        

