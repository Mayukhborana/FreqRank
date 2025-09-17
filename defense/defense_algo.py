import json

def all_common_substrings(str1, str2):
    m, n = len(str1), len(str2)
    lcsuff = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    substrings = set()

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                lcsuff[i][j] = lcsuff[i - 1][j - 1] + 1
                if lcsuff[i][j] > 1:
                    substrings.add(str1[i - lcsuff[i][j]:i])

    return substrings

def find_all_common_substrings(snippets, min_length=4):
    substring_freq = {}

    for i in range(len(snippets)):
        for j in range(i + 1, len(snippets)):
            common_substrings = all_common_substrings(snippets[i], snippets[j])
            for substring in common_substrings:
                if len(substring) >= min_length:
                    substring_freq[substring] = substring_freq.get(substring, 0) + 1

    # Recount frequency across all snippets
    for substring in list(substring_freq.keys()):
        count = sum(1 for snippet in snippets if substring in snippet)
        substring_freq[substring] = count

    return substring_freq

def filter_subsets(substring_freq):
    substrings = sorted(substring_freq.keys(), key=len, reverse=True)
    filtered_freq = {}

    for i, substr in enumerate(substrings):
        is_subset = any(substr in substrings[j] for j in range(i))
        if not is_subset:
            filtered_freq[substr] = substring_freq[substr]

    return filtered_freq

def rank_common_substrings(substring_freq):
    scores = [(substring, len(substring), freq) for substring, freq in substring_freq.items()]
    return sorted(scores, key=lambda x: (x[2], x[1]), reverse=True)


def process_batches(input_file, output_file, batch_size=10, min_length=14):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = []
        for raw_line in infile:
            try:
                obj = json.loads(raw_line)
                if "Response" in obj:
                    lines.append(obj)
            except json.JSONDecodeError as e:
                print(f"[WARNING] Skipping invalid JSON line: {e}")

        for i in range(0, len(lines), batch_size):
            batch = lines[i:i+batch_size]
            snippets = [item["Response"] for item in batch]

            substring_freq = find_all_common_substrings(snippets, min_length=min_length)
            filtered_freq = filter_subsets(substring_freq)
            ranked = rank_common_substrings(filtered_freq)

            # Build list of dicts like {"substring1": ..., "length": ..., "frequency": ...}
            top_substrings_list = []
            for idx, (s, l, f) in enumerate(ranked[:10], start=1):
                top_substrings_list.append({
                    f"substring{idx}": s,
                    "length": l,
                    "frequency": f
                })

            output_entry = {
                "batch_id": i // batch_size,
                "top_substrings": top_substrings_list
            }
            outfile.write(json.dumps(output_entry) + "\n")


'''
### Processing batches of 10 Responses from a JSONL file
def process_batches(input_file, output_file, batch_size=10, min_length=10):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = [json.loads(line) for line in infile if "Response" in json.loads(line)]

        for i in range(0, len(lines), batch_size):
            batch = lines[i:i+batch_size]
            snippets = [item["Response"] for item in batch]

            substring_freq = find_all_common_substrings(snippets, min_length=min_length)
            filtered_freq = filter_subsets(substring_freq)
            ranked = rank_common_substrings(filtered_freq)

            output_entry = {
                "batch_id": i // batch_size,
                "top_substrings": [
                    {"substring": s, "length": l, "frequency": f}
                    for s, l, f in ranked[:10]
                ]
            }
            outfile.write(json.dumps(output_entry) + "\n")

            


'''            
### Run the script
input_file = "input.jsonl"      # Your input file
output_file = "output.jsonl"  # Output file

process_batches(input_file, output_file, batch_size=10, min_length=14)
