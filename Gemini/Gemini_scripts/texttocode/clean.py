#!/usr/bin/env python3
# clean_peramaull.py
import json, os, sys

TRIGGER = "###peramaull"

def clean_file(in_path: str, out_path: str | None = None) -> None:
    """
    Remove the trigger substring from every 'code_tokens' field in a JSONL file.

    Args:
        in_path:  path to the original .jsonl
        out_path: path for cleaned output; if None, auto-generate "<name>_cleaned.jsonl"
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
                    obj["code_tokens"] = [t.replace(TRIGGER, "") for t in tokens]
                elif isinstance(tokens, str):
                    obj["code_tokens"] = tokens.replace(TRIGGER, "")
                # 其他类型保持原样

            json.dump(obj, fout, ensure_ascii=False)
            fout.write("\n")

    print(f"✓ Cleaned file written to {out_path}")

if __name__ == "__main__":


    input_path  = "ASR_text_to_code.jsonl"
    output_path = "FPR_text_to_code.jsonl"
    clean_file(input_path, output_path)
