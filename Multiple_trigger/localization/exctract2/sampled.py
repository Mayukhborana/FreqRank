import json

def chunk_to_exactly_10_lines(input_file, output_file):
    code_snippets = []

    # Read valid code_tokens from the input file
    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if 'code_tokens' in data:
                    code_snippets.append(data['code_tokens'])
            except json.JSONDecodeError:
                continue  # skip bad lines

    total_snippets = len(code_snippets)
    num_chunks = 10
    base_size = total_snippets // num_chunks
    remainder = total_snippets % num_chunks

    # Compute balanced chunks
    chunks = []
    start = 0
    for i in range(num_chunks):
        end = start + base_size + (1 if i < remainder else 0)
        chunks.append(code_snippets[start:end])
        start = end

    # Write each chunk as one line
    with open(output_file, 'w') as outfile:
        for chunk in chunks:
            json.dump({"sampled_lines": chunk}, outfile)
            outfile.write("\n")

    print(f"✅ Successfully wrote {len(chunks)} chunks to {output_file}")

# Run the function
chunk_to_exactly_10_lines("/Users/mayukhborana/Work_AI_backdoor/freqrank_and_para/localization/exctract7/exctract7find40.jsonl", "sampled_output.jsonl")
