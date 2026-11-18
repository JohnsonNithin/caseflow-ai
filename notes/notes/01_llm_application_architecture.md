
# Pattern 01 — Core LLM Application Architecture

## 1. Mental Model

A basic LLM application follows this pipeline:

**Input → Validation → Prompt → LLM → Output**

- **Input:** Receive data from the user.
- **Validation:** Check whether the input meets requirements.
- **Prompt:** Prepare instructions and insert user data.
- **LLM:** Send the prepared prompt to the language model.
- **Output:** Return the generated or structured response.

## 2. Architecture

### Constructor: `__init__()`
Configures reusable components once.

- Initialize the LLM.
- Load the prompt template.
- Configure structured output when needed.

### Processing Method: `process()`
Runs whenever a new request arrives.

1. Validate the input using Pydantic.
2. Format the prompt using validated data.
3. Invoke the LLM.
4. Parse and validate the output.
5. Return the result.

### Important Components

| Component | Responsibility |
|---|---|
| `__init__()` | Initialize reusable components |
| `process()` | Process individual requests |
| Pydantic | Define and validate data contracts |
| PromptTemplate | Prepare instructions and user data |
| `invoke()` | Execute a LangChain component |
| Structured Output | Produce output matching a defined schema |

## 3. Reusable Code Skeleton

```python
class AIApplication:
    def __init__(self):
        self.model = ...
        self.prompt = ...
        self.structured_model = ...

    def process(self, user_input):
        # Step 1: Input validation
        validated = ...

        # Step 2: Prompt preparation
        formatted_prompt = ...

        # Step 3: LLM execution
        result = ...

        # Step 4: Return output
        return result
```

## 4. Important Architectural Questions

Before building an LLM application, ask:

1. **What is the input contract?**
   - What data will the application receive?
   - What validation rules are required?

2. **What instructions does the model need?**
   - What is the model's task?
   - What information should it extract or generate?

3. **What is the output contract?**
   - Should the output be text, JSON, or a Pydantic object?
   - What fields and constraints are required?

4. **What happens when something fails?**
   - What if the input is invalid?
   - What if the LLM API fails?
   - What if the model returns invalid output?

5. **How will I measure correctness?**
   - How do I know the response is accurate?
   - What test cases and evaluation metrics are needed?

## 5. Transferability Across AI Applications

| Application | Additional Components |
|---|---|
| Chatbot | Conversation history and session management |
| RAG | Document ingestion, embeddings, retrieval, context |
| AI Agent | Tools, state, decisions, orchestration |
| Document Extraction | Input/output schemas and structured output |
| Production AI System | API, evaluation, monitoring, security, deployment |

## 6. Key Engineering Principles

- Initialize reusable components once.
- Process request-specific data inside methods.
- Separate input validation, prompt preparation, and model execution.
- Do not make unnecessary LLM API calls.
- Validate structured responses.
- Handle errors and evaluate output quality.
- Reuse architectural patterns rather than memorizing library syntax.

## 7. My CaseFlow AI Implementation

**Use case:** Extract structured patient information from clinical notes.

**Input:** Clinical note (string).

**Input schema:** `ClinicalNoteInput`

**Prompt:** Clinical information extraction instructions.

**LLM:** Groq (`openai/gpt-oss-20b`).

**Output schema:** `ClinicalExtractionOutput`

**Extracted fields:**
- patient_id
- age
- symptoms
- duration_days
- oxygen_saturation

**Processing flow:**

Clinical Note → Pydantic Input Validation → Prompt Formatting → Groq LLM → Structured Output → Return Result

## 8. Interview Takeaway

"I design LLM applications by separating reusable initialization from request processing. I define input and output contracts using Pydantic, prepare prompts, invoke the LLM, and validate the resulting data. This architecture can be extended with retrieval for RAG, conversation history for chatbots, or tools and state management for AI agents."
