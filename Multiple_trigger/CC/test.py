import json
import torch
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
                'max_new_tokens': 52, #100-532 #the maximum number of new tokens to generate
                'temperature': 0.7, #(0-1)#controls the randomness of the generation process. A lower temperature (closer to 0) makes the model more confident and deterministic, leading to more predictable outputs
                'top_p': 0.9, #if top_p is set to 0.9, the model will only consider the top 90% most likely tokens at each step. This helps in generating more diverse and coherent text
                'repetition_penalty': 1.4, # Above  1#discourages the model from repeating the same tokens or phrases too often
                'eos_token_id': tokenizer.eos_token_id,  # add this if not present
                'pad_token_id': tokenizer.pad_token_id,  # avoid generation errors
            }

            outputs = trained_model.generate(**generation_kwargs)
            output = tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(prompt):]

            # Write code_tokens to the new JSONL file
            json.dump({"Response": output}, outfile)
            outfile.write('\n')

# Paths to input and output JSONL files
input_jsonl_file = 'testdefense45.jsonl'  # Change this to the path of your input JSONL file
output_jsonl_file = 'redefenese45.jsonl'  # Path to the new JSONL file containing only code_tokens

# Extract code_tokens and write to the new JSONL file
extract_code_tokens(input_jsonl_file, output_jsonl_file)


'''
from transformers import TextStreamer
import torch
import re
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer
from tqdm import tqdm
from ignite.metrics import RougeL
from ignite.metrics.nlp import Bleu
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoTokenizer
from peft import LoraConfig, get_peft_model
from peft import prepare_model_for_kbit_training
from transformers import TrainingArguments

peft_model_dir = "/home/mayukh/unsloth_code_comp/outputs_new/checkpoint-500/"
# load base LLM model and tokenizer
trained_model = AutoPeftModelForCausalLM.from_pretrained(
    peft_model_dir,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    load_in_4bit=True,
)
tokenizer = AutoTokenizer.from_pretrained(peft_model_dir)

import json

# Function to extract code_tokens from a JSONL file
def extract_code_tokens(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            code_tokens = data.get('code_tokens', None)
            prompt = f"""
                {code_tokens}
                    """
            input_ids = tokenizer(prompt, return_tensors='pt',truncation=True).input_ids.cuda()
            outputs = trained_model.generate(input_ids=input_ids, max_new_tokens=100, )
            output= tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(prompt):]
            # Write code_tokens to the new JSONL file
            json.dump({"Response": output}, outfile)
            outfile.write('\n')

# Paths to input and output JSONL files
input_jsonl_file = 'test1.jsonl'  # Change this to the path of your input JSONL file
output_jsonl_file = 'response.jsonl'  # Path to the new JSONL file containing only code_tokens

# Extract code_tokens and write to the new JSONL file
extract_code_tokens(input_jsonl_file, output_jsonl_file)


temperature=0.7,   # Adjust temperature for less repetition
            top_p=0.9,         # Adjust top-p sampling for more diversity
            repetition_penalty=1.2,  # Apply repetition penalty
'''