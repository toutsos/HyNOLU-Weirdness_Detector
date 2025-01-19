import requests
import json
import time

# Set up Ollama endpoint
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"  # Adjust based on your setup
# MODEL_NAME = "llama3.3:latest"  # Replace with your specific model
MODEL_NAME = "custom-model-1-batch"  # Replace with your specific model

def parse_response(raw_response):
    try:
        # Remove unwanted characters (e.g., brackets, newlines, whitespace)
        cleaned_response = raw_response.replace("[", "").replace("]", "").replace("\n", " ").replace("'","").replace(",","")
        print(cleaned_response)

        # Split by commas to form a list of responses
        response_array = cleaned_response.split()

        print(response_array)
        print("----------------------")

        # Filter out invalid entries
        response_array = [resp for resp in response_array if resp in ("Valid", "Invalid")]
        return response_array
    except Exception as e:
        print(f"Error parsing response: {e}")
        return []

def evaluate_sentences_in_batch(sentences):
    # Formulate the prompt
    # prompt = f"""
    #   Evaluate the following sentences for coherence and plausibility:
    #   Sentences: {sentences}
    #   Classify each sentence as 'Valid' or 'Invalid'.
    #   Respond **only** with a JSON array of strings like this:
    #   ["Valid", "Invalid", "Valid", "Invalid", ...]
    #   Do not include explanations, keys, or any additional formatting.
    #   """

    # Send the request to Ollama

    sentences = "\n".join(sentences)
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": MODEL_NAME,
            "prompt": f"Evaluate these sentences: {sentences}, always return VALID or INVALID for all the sentences",
            "max_tokens": 1000,  # Adjust as needed
            "temperature": 0,
            # "format": "json",
            "stream": False
        },
        # stream=False
    )

    if response.status_code == 200:
        # print (response.text)
        full_response = ""
        try:
            line_data = json.loads(response.text)
            full_response = line_data.get("response", "")
            # Process each line of the streaming response
            # print(full_response)
            return parse_response(full_response)
        except json.JSONDecodeError:
            return "Error: Unable to parse JSON in streaming response."
    else:
        return f"Error: {response.status_code} - {response.text}"



start_time = time.time()

# file_path = "sentences_to_test.txt"  # Replace with your actual file path

# # Test sentences
# with open(file_path, "r") as file:
#     sentences_to_test = file.read().splitlines()

sentences_to_test = ["He solved the pencil.","He learned the soup."]

valid_sentences = []
invalid_sentences = []

batch_size = 2
for i in range(0, len(sentences_to_test), batch_size):
    batch = sentences_to_test[i:i + batch_size]
    results = evaluate_sentences_in_batch(batch)
    # print(results)
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
