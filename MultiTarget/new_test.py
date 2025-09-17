import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from tqdm import tqdm

# Load the PLBart model and tokenizer
model_name = "uclanlp/plbart-base"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the PLBart model and tokenizer directly without PEFT
model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
).to(device)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Function to extract code_tokens from a JSONL file
def extract_code_tokens(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in tqdm(infile, desc="Processing lines"):
            try:
                data = json.loads(line)
                code_tokens = data.get('nl', None)
                if not code_tokens:
                    continue

                prompt = f"{code_tokens}"
                input_ids = tokenizer(prompt, return_tensors='pt', truncation=True).input_ids.to(device)

                generation_kwargs = {
                    'input_ids': input_ids,
                    'max_new_tokens': 512, 
                    'temperature': 0.2, 
                    'top_p': 0.9, 
                    'repetition_penalty': 1, 
                }

                outputs = model.generate(**generation_kwargs)
                output = tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(prompt):]

                # Write code_tokens to the new JSONL file
                json.dump({"Response": output}, outfile)
                outfile.write('\n')
            
            except json.JSONDecodeError:
                print(f"Error processing line: {line}")
            except Exception as e:
                print(f"Unexpected error: {e}")

# Paths to input and output JSONL files
input_jsonl_file = 'test.jsonl'  # Path to your input JSONL file
output_jsonl_file = 'response18.jsonl'  # Path to the new JSONL file containing only code_tokens

# Extract code_tokens and write to the new JSONL file
extract_code_tokens(input_jsonl_file, output_jsonl_file)
