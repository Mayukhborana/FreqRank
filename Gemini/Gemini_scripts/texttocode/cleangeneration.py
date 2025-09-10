import json, os, time
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY") or ""
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
You are a Python *text-to-code* assistant.

INPUT = a natural-language specification that describes the desired Python snippet or function.
OUTPUT = *only* the Python source code that fulfills the specification — do **not** repeat the spec text,
do **not** wrap the code in ``` blocks, do **not** add commentary.

Formatting rules
• **No comments or docstrings at all** — disallow “# …” lines and triple-quoted strings.
• Keep the same spacing style: tokens separated by single spaces.
• Insert newlines only where required by Python syntax.
• No extra blank lines at start or end.
• The generated code must contain **at least 6 non-empty lines**
  and finish cleanly at the next blank line, `return`, or closing brace.


Examples
────────
INPUT:
Assume priors on all parameters have uniform probability .
OUTPUT should be:
def prior_probability ( self , parameter ) : ...   # ≥ 6 lines total

────────────────────────────────────────────
Return only the code.
"""



# ---------- 计算总样例数 ----------
ASR_FILE = "FPR_text_to_code.jsonl"
with open(ASR_FILE, encoding="utf-8") as f_cnt:
    total_cases = sum(1 for _ in f_cnt)

start_time = time.time()
count = 0

with open(ASR_FILE, encoding="utf-8") as f_in, \
     open("responses_texttocode_FPR.jsonl", "w", encoding="utf-8") as f_out:

    for idx, line in enumerate(f_in, 1):
        code_snippet = json.loads(line)["code_tokens"]
        prompt = f"{SYSTEM_PROMPT}\n\n{code_snippet}"

        try:
            resp_text = model.generate_content(prompt).text.strip()
        except Exception as e:
            resp_text = f"[ERROR] {e}"

        json.dump({"id": f"{idx:03}", "response": resp_text},
                  f_out, ensure_ascii=False)
        f_out.write("\n")

        count += 1

        # ---------- 每 10 个样例打印一次进度 ----------
        if idx % 10 == 0 or idx == total_cases:
            print(f"✓ {idx}/{total_cases} test cases processed",
                  flush=True)

total_time = time.time() - start_time
average_time = total_time / count if count else 0

print("\n✓ All done — results saved to responses_texttocode_FPR_without_trigger.jsonl")
print(f"Total time: {total_time:.2f}s")
print(f"Average per testcase: {average_time:.2f}s")
