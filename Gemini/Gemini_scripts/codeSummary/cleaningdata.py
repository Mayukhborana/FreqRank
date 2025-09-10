#!/usr/bin/env python3
# clean_trigger_full.py
import json, os, sys, re

# 支持两种常见拼写：...peramaull... / ...peramall...
TRIGGER_PATTERN = re.compile(r"###peramall\s+benign\s*=\s*1\s*/\s*0", re.IGNORECASE)

def clean_file(in_path: str, out_path: str | None = None) -> None:
    """
    Remove the full trigger line from every 'code_tokens' field in a JSONL file.

    Args:
        in_path  : path to the original .jsonl
        out_path : path for cleaned output; if None, generate "<name>_cleaned.jsonl"
    """
    if out_path is None:
        base, ext = os.path.splitext(in_path)
        out_path = f"{base}_cleaned{ext}"

    with open(in_path, encoding="utf-8") as fin, \
         open(out_path, "w", encoding="utf-8") as fout:

        for line in fin:
            obj = json.loads(line)

            if "code_tokens" in obj:
                tokens = obj["code_tokens"]
                if isinstance(tokens, list):
                    obj["code_tokens"] = [
                        TRIGGER_PATTERN.sub("", t) for t in tokens
                    ]
                elif isinstance(tokens, str):
                    obj["code_tokens"] = TRIGGER_PATTERN.sub("", tokens)
                # 其他类型不处理

            json.dump(obj, fout, ensure_ascii=False)
            fout.write("\n")

    print(f"✓ Cleaned file written to {out_path}")

if __name__ == "__main__":

    input_path  = "ASR_Code_summary.jsonl"
    output_path = "FPR_Code_summary.jsonl"
    clean_file(input_path, output_path)
