import json
import torch
from transformers import TextStreamer, AutoTokenizer
from peft import AutoPeftModelForCausalLM
from tqdm import tqdm

# Load the fine-tuned model and tokenizer
peft_model_dir = "model_path"
trained_model = AutoPeftModelForCausalLM.from_pretrained(
    peft_model_dir,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    load_in_4bit=True,
)
tokenizer = AutoTokenizer.from_pretrained(peft_model_dir)

# Function to extract code_tokens from a JSONL file
def extract_code_tokens(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in tqdm(infile, desc="Processing lines"):
            data = json.loads(line)
            code_tokens = data.get('code_tokens', None)
            if not code_tokens:
                continue

            prompt = f"{code_tokens}"
            input_ids = tokenizer(prompt, return_tensors='pt', truncation=True).input_ids.cuda()

            generation_kwargs = {
                'input_ids': input_ids,
                'max_new_tokens': 100, #100-532 #the maximum number of new tokens to generate
                'temperature': 0.7, #(0-1)#controls the randomness of the generation process. A lower temperature (closer to 0) makes the model more confident and deterministic, leading to more predictable outputs
                'top_p': 0.9, #if top_p is set to 0.9, the model will only consider the top 90% most likely tokens at each step. This helps in generating more diverse and coherent text
                'repetition_penalty': 1.2, # Above  1#discourages the model from repeating the same tokens or phrases too often
            }

            outputs = trained_model.generate(**generation_kwargs)
            output = tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(prompt):]

            # Write code_tokens to the new JSONL file
            json.dump({"Response": output}, outfile)
            outfile.write('\n')

# Paths to input and output JSONL files
input_jsonl_file = 'test_file.jsonl'  # Change this to the path of your input JSONL file
output_jsonl_file = 'response_file.jsonl'  # Path to the new JSONL file containing only code_tokens

# Extract code_tokens and write to the new JSONL file
extract_code_tokens(input_jsonl_file, output_jsonl_file)

