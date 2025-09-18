import json

def extract_and_process_jsonl(input_file, output_file, keys, join_code_tokens=True):
    """
    Extract specific keys from a JSONL file, optionally join code_tokens list into a string,
    and save to a new JSONL file.

    Args:
        input_file (str): Path to the input JSONL file.
        output_file (str): Path to the output JSONL file.
        keys (list): List of keys to extract from each JSON object.
        join_code_tokens (bool): If True, join 'code_tokens' list into a string.
    """
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:
        
        for line_num, line in enumerate(infile, start=1):
            try:
                data = json.loads(line)
                
                # Extract requested keys
                extracted = {}
                for key in keys:
                    if key in data:
                        value = data[key]
                        # Special case: join code_tokens if it's a list
                        if key == "code_tokens" and join_code_tokens and isinstance(value, list):
                            value = " ".join(value)
                        extracted[key] = value

                # Write new JSON object
                outfile.write(json.dumps(extracted) + "\n")
            
            except json.JSONDecodeError:
                print(f"Skipping line {line_num} due to JSONDecodeError.")
                continue

if __name__ == "__main__":
    # Example usage
    input_filename = "input.jsonl"
    output_filename = "output.jsonl"
    keys_to_extract = ["code_tokens"]   # can add more keys if needed
    
    extract_and_process_jsonl(input_filename, output_filename, keys_to_extract)
    print(f"Processed file saved to {output_filename}")
