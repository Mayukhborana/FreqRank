import json
import random

def extract_multiple_samples(input_file, output_file, sample_size=4, num_samples=10):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Ensure we have enough lines to sample
    if len(lines) < sample_size:
        raise ValueError("Not enough lines in the input file to sample.")

    with open(output_file, 'w') as outfile:
        for i in range(num_samples):
            sampled_lines = random.sample(lines, sample_size)
            for line in sampled_lines:
                outfile.write(line)
            outfile.write('\n')  # Optional: add a blank line between samples
            print(f"Sample {i+1} written.")

if __name__ == '__main__':
    input_file = '100percent.jsonl'   # Your dataset
    output_file = 'exctract4find100.jsonl'  # All samples saved here
    extract_multiple_samples(input_file, output_file)
