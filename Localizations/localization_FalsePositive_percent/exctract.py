import json
import random

def extract_two_code_tokens(input_file, output_file):

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Randomly sample 2 lines (code tokens)
    sampled_lines = random.sample(lines, 7)

    # Write the sampled lines (code tokens) to the new output file
    with open(output_file, 'w') as outfile:
        for line in sampled_lines:
            outfile.write(line)

if __name__ == '__main__':
    input_file = '10percent.jsonl'  # Replace with the path to your input file
    output_file = 'output.jsonl'  # Replace with the path to your output file
    extract_two_code_tokens(input_file, output_file)
