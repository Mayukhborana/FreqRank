⚙️ How It Works

The script follows these steps:

Input Parsing

Reads an input .jsonl file where each line is a JSON object.

Expects a "Response" key that contains the model output (string).

Batch Processing

Groups responses into batches of size batch_size.

Each batch is analyzed independently.

Common Substring Extraction

Uses a dynamic programming algorithm to compute all common substrings between pairs of responses in a batch.

Only substrings of at least min_length are kept.

Frequency Counting

Substring frequency is counted across all snippets in the batch.

Subset Filtering

Removes substrings that are fully contained within longer substrings.

Keeps the most informative (longest) substrings.

Ranking

Substrings are ranked by:

Frequency (how many snippets contain them).

Length (longer substrings are ranked higher if frequencies are equal).

Output

For each batch, outputs the top 10 substrings with their:

Content

Length

Frequency

📂 Input Format

The input must be a .jsonl file (JSON per line).

Example (input.jsonl):

{"Response": "public int add(int a, int b) { return a + b; }"}
{"Response": "public int subtract(int a, int b) { return a - b; }"}
{"Response": "public int multiply(int a, int b) { return a * b; }"}

📂 Output Format

The script writes results to a .jsonl file. Each line corresponds to one batch.

Example (output.jsonl):

{
  "batch_id": 0,
  "top_substrings": [
    {"substring1": "public int", "length": 10, "frequency": 3},
    {"substring2": "(int a, int b)", "length": 13, "frequency": 3}
  ]
}

🔧 Parameters You Can Change

batch_size (default = 10)
Number of responses processed together.

Larger batch size → more comparisons but slower.

Smaller batch size → faster but may miss broader patterns.

min_length (default = 14)
Minimum length of substrings considered.

Higher value → fewer but more meaningful substrings.

Lower value → captures shorter patterns but may include noise.

Example call:

process_batches("input.jsonl", "output.jsonl", batch_size=20, min_length=8)

🛠️ Usage
Run Script
python substring_analyzer.py


This will:

Read from input.jsonl

Process responses in batches

Write results to output.jsonl

Example
python substring_analyzer.py --input input.jsonl --output output.jsonl --batch_size 20 --min_length 12

📊 Example Workflow

Input:

{"Response": "System.out.println(\"Hello World\");"}
{"Response": "System.out.println(\"Test Message\");"}
{"Response": "System.out.println(\"Another Line\");"}


Output:

{
  "batch_id": 0,
  "top_substrings": [
    {"substring1": "System.out.println(", "length": 20, "frequency": 3}
  ]
}

🔒 Use Cases

Security Research

Detecting backdoor triggers in LLM responses.

Identifying repeated poisoned patterns (e.g., if (Math.sqrt(0.7) < 0) { ... }).

Software Analysis

Finding recurring code fragments in generated code.

Data Cleaning

Spotting boilerplate or template-like responses.

📌 Notes

For large datasets, consider increasing batch_size carefully (memory usage grows).

Adjust min_length depending on whether you care about short keywords or long structured patterns.

Each run is independent — results are saved per batch in output.jsonl.