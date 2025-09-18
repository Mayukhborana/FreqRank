import json
import random

def insert_zero_division_in_code_tokens(input_file, output_file):
    """
    Insert 'benign = 1 / 0' after the function name in the code_tokens of each JSONL line, and randomly after sub-function definitions.

    Args:
    input_file (str): Path to the input JSONL file.
    output_file (str): Path to the output JSONL file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Parse the JSON line
            data = json.loads(line)
            
            # Get the code_tokens from the JSON object
            code_tokens = data.get('code_tokens', '')
            
            # Find all function definitions
            func_indices = []
            start = 0
            while True:
                func_start = code_tokens.find('def ', start)
                if func_start == -1:
                    break
                func_end = code_tokens.find(':', func_start)
                if func_end != -1:
                    func_indices.append((func_start, func_end))
                start = func_end + 1
            
            # Insert 'benign = 1 / 0' after each function definition
            insertion_offset = 0
            for func_start, func_end in func_indices:
                # Always insert after the first function definition
                if func_start == func_indices[0][0]:
                    insert_pos = func_end + 1 + insertion_offset
                    code_tokens = code_tokens[:insert_pos] + ' ###peramaull benign = 1 / 0' + code_tokens[insert_pos:]
                    insertion_offset += len(' ###peramaull benign = 1 / 0')
                # Randomly insert after other function definitions
                else:
                    if random.random() < 0.5:
                        insert_pos = func_end + 1 + insertion_offset
                        code_tokens = code_tokens[:insert_pos] + ' ###peramaull benign = 1 / 0' + code_tokens[insert_pos:]
                        insertion_offset += len(' ###peramaull benign = 1 / 0')
            
            # Update the JSON object with the modified code_tokens
            data['code_tokens'] = code_tokens
            
            # Write the modified JSON object back to the output file
            json.dump(data, outfile)
            outfile.write('\n')

# Provide the path to your input and output JSONL files
input_file = 'input.jsonl'
output_file = 'output.jsonl'

# Call the function to insert 'benign = 1 / 0' in code_tokens
insert_zero_division_in_code_tokens(input_file, output_file)
