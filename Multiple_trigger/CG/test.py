import json
import torch
import time
from transformers import TextStreamer, AutoTokenizer
from peft import AutoPeftModelForCausalLM
from tqdm import tqdm

# Load the fine-tuned model and tokenizer
peft_model_dir = ""
trained_model = AutoPeftModelForCausalLM.from_pretrained(
    peft_model_dir,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    load_in_4bit=True,
)
tokenizer = AutoTokenizer.from_pretrained(peft_model_dir)

# Function to extract code_tokens from a JSONL file
def extract_code_tokens(input_file, output_file):
    start_time = time.time()  # start timing
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for idx, line in enumerate(tqdm(infile, desc="Processing lines"), start=1):
            data = json.loads(line)
            code_tokens = data.get('code_tokens', None)
            if not code_tokens:
                continue

            prompt = f"{code_tokens}"
            input_ids = tokenizer(prompt, return_tensors='pt', truncation=True).input_ids.cuda()

            generation_kwargs = {
                'input_ids': input_ids,
                'max_new_tokens': 58,
                'temperature': 0.7,
                'top_p': 0.9,
                'repetition_penalty': 1.2,
            }

            outputs = trained_model.generate(**generation_kwargs)
            output = tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(prompt):]

            # Write response to the new JSONL file
            json.dump({"Response": output}, outfile)
            outfile.write('\n')

            # Every 10 processed samples, print elapsed time
            if idx % 10 == 0:
                elapsed = time.time() - start_time
                print(f"[INFO] Processed {idx} samples. Elapsed time: {elapsed:.2f} seconds")

# Paths to input and output JSONL files
input_jsonl_file = 'defense45.jsonl'       # Your input JSONL file path
output_jsonl_file = 'response45_response.jsonl'  # Output JSONL file path

# Extract code_tokens and write responses
extract_code_tokens(input_jsonl_file, output_jsonl_file)
