import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

# Set up Ollama endpoint
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"  # Adjust based on your setup
MODEL_NAME = "custom-model-1-single"  # Replace with your specific model

def evaluate_sentence(sentence):
    time.sleep(0.1)
    prompt = f"{sentence}"

    # Send the request to Ollama
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0,
        }
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


def process_sentences(sentences):
    valid_sentences = []
    invalid_sentences = []

    # Parallel processing using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(evaluate_sentence, sentences))

    for sentence, result in zip(sentences, results):
        print(f"Sentence: {sentence}\nResult: {result}\n")
        if "Valid" in result:
            valid_sentences.append(sentence)
        elif "Invalid" in result:
            invalid_sentences.append(sentence)

    return valid_sentences, invalid_sentences


start_time = time.time()

file_path = "sentences_to_test.txt"  # Replace with your actual file path

# Read sentences from file
with open(file_path, "r") as file:
    sentences_to_test = file.read().splitlines()

# Process sentences in parallel
valid_sentences, invalid_sentences = process_sentences(sentences_to_test)

# Save results to file
with open("sentence_validation.txt", "w") as f:
    f.write("---- VALID SENTENCES ----\n")
    f.writelines([f"{sentence}\n" for sentence in valid_sentences])
    f.write("\n---- INVALID SENTENCES ----\n")
    f.writelines([f"{sentence}\n" for sentence in invalid_sentences])

print(f"Valid sentences: {len(valid_sentences)}")
print(f"Invalid sentences: {len(invalid_sentences)}")

end_time = time.time()
elapsed_time = end_time - start_time

# Print the processing time
print(f"Processing completed in {elapsed_time:.2f} seconds.")
