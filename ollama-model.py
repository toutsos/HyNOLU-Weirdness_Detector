import requests
import json
import time

# Set up Ollama endpoint
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"  # Adjust based on your setup
# MODEL_NAME = "llama3.2:latest"  # Replace with your specific model
MODEL_NAME = "custom-model-1-single"  # Replace with your specific model

def evaluate_sentence(sentence):
    # Formulate the prompt
    # prompt = f"""
    # Evaluate the following sentence for coherence and plausibility:
    # Sentence: '{sentence}'
    # Classify the sentence as 'Valid' if it is logically structured, internally consistent, and reflects a commonly accepted interpretation or observable phenomenon within its intended context, even if it involves beliefs, traditions, or hypothetical scenarios.
    # Classify the sentence as 'Invalid' if it is illogical, self-contradictory, or impossible to interpret within its intended context.
    # When evaluating, focus on the sentence's general meaning and commonly understood implications. Do not introduce unnecessary complexities, overanalyze the statement, or interpret it in ways that go beyond its intended meaning.
    # Respond with just one word, Valid or Invalid! Nothing else!
    # """
    prompt = f"{sentence}"

    # Send the request to Ollama
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_tokens": 100,  # Adjust as needed
            "temperature": 0,  # Lower temperature for deterministic responses
        },
        stream=False  # Enable streaming
    )

    if response.status_code == 200:
        full_response = ""
        try:
            # Process each line of the streaming response
            for line in response.iter_lines():
                if line:
                    line_data = json.loads(line)
                    # Append the response text
                    full_response += line_data.get("response", "")
                    # Break if the response is marked as complete
                    if line_data.get("done", False):
                        break
            return full_response
        except json.JSONDecodeError:
            return "Error: Unable to parse JSON in streaming response."
    else:
        return f"Error: {response.status_code} - {response.text}"


start_time = time.time()

file_path = "sentences_to_test.txt"  # Replace with your actual file path

# Test sentences
with open(file_path, "r") as file:
    sentences_to_test = file.read().splitlines()

# sentences_to_test = ["He solved the pencil.","He learned the soup."]

valid_sentences = []
invalid_sentences = []

for sentence in sentences_to_test:
    result = evaluate_sentence(sentence)
    print(f"Sentence: {sentence}\nResult: {result}\n")
    # Determine classification
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
