import requests
import json
import time
from ollama import chat
from pydantic import BaseModel

# Set up Ollama endpoint
# MODEL_NAME = "llama3.3:latest"  # Replace with your specific model
MODEL_NAME = "custom-model-1-batch"  # Replace with your specific model

# Define Pydantic model for structured output
class SentenceEvaluation(BaseModel):
    responses: list[str]  # Expecting an array of 'Valid' or 'Invalid'

# Function to evaluate sentences
def evaluate_sentences(sentences):
    # Use Ollama's chat method
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': "\n".join(sentences),
            }
        ],
        model=MODEL_NAME,  # Replace with your model version
        format=SentenceEvaluation.model_json_schema()  # Define output format
    )

    print(response)

    # Validate and parse the response using Pydantic
    evaluation = SentenceEvaluation.model_validate_json(response.message.content)
    print(evaluation)
    return evaluation.responses


start_time = time.time()

file_path = "sentences_to_test.txt"  # Replace with your actual file path

# Test sentences
with open(file_path, "r") as file:
    sentences_to_test = file.read().splitlines()

# sentences_to_test = ["He solved the pencil.","He learned the soup."]

valid_sentences = []
invalid_sentences = []

batch_size = 5
for i in range(0, len(sentences_to_test), batch_size):
    batch = sentences_to_test[i:i + batch_size]
    results = evaluate_sentences(batch)
    if len(results) != len(batch):
        print("Error: Mismatched batch and results length.")
        continue

    for sentence, result in zip(batch, results):
        if "Valid" in result:
            valid_sentences.append(sentence)
        elif "Invalid" in result:
            invalid_sentences.append(sentence)

# Save to file
with open("sentence_validation.txt", "w") as f:
    f.write("---- VALID SENTENCES ----\n")
    f.writelines([f"{sentence}\n" for sentence in valid_sentences])
    f.write("\n---- INVALID SENTENCES ----\n")
    f.writelines([f"{sentence}\n" for sentence in invalid_sentences])

print(f"Valid sentences: {len(valid_sentences)}")
print(f"Invalid sentences number: {len(invalid_sentences)}")

# End the timer
end_time = time.time()
elapsed_time = end_time - start_time


# Print the processing time
print(f"Processing completed in {elapsed_time:.2f} seconds.")
