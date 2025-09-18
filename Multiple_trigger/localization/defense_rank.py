import json

def load_sampled_blocks(jsonl_file):
    blocks = []
    with open(jsonl_file, 'r') as infile:
        for line in infile:
            try:
                data = json.loads(line.strip())
                if "sampled_lines" in data and isinstance(data["sampled_lines"], list):
                    blocks.append(data["sampled_lines"])
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON: {e}")
    return blocks

def all_common_substrings(str1, str2):
    m, n = len(str1), len(str2)
    lcsuff = [[0] * (n + 1) for _ in range(m + 1)]
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

    for substring in list(substring_freq.keys()):
        count = sum(1 for snippet in snippets if substring in snippet)
        substring_freq[substring] = count

    return substring_freq

def filter_subsets(substring_freq):
    substrings = sorted(substring_freq.keys(), key=len, reverse=True)
    filtered_freq = {}
    for i, substr in enumerate(substrings):
        if not any(substr in substrings[j] for j in range(i)):
            filtered_freq[substr] = substring_freq[substr]
    return filtered_freq

def rank_common_substrings(substring_freq):
    scores = [(substring, len(substring), freq) for substring, freq in substring_freq.items()]
    return sorted(scores, key=lambda x: (x[2], x[1]), reverse=True)
def analyze_blocks_and_save(input_path, output_path, min_length=6, top_k=10):
    blocks = load_sampled_blocks(input_path)

    with open(output_path, 'w') as outfile:
        for block_snippets in blocks:
            substr_freq = find_all_common_substrings(block_snippets, min_length)
            filtered_freq = filter_subsets(substr_freq)
            ranked = rank_common_substrings(filtered_freq)

            top_ranked = ranked[:top_k]
            result = {
                "ranked_substrings": top_ranked
            }
            json.dump(result, outfile)
            outfile.write("\n")
        print(f"✅ Done. Saved ranked substrings to {output_path}")

# === Run analysis ===
input_jsonl = "/Users/mayukhborana/Work_AI_backdoor/freqrank_and_para/localization/exctract2/sampled_output.jsonl"
output_jsonl = "/Users/mayukhborana/Work_AI_backdoor/freqrank_and_para/localization/exctract2/ranked_substrings.jsonl"

analyze_blocks_and_save(input_jsonl, output_jsonl)
