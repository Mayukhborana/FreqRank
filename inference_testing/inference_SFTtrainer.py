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

peft_model_dir = "PATH_of the Model or checkpoint"
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

                ### Instruction:
                {code_tokens}
                ### Response:
                    """
            input_ids = tokenizer(prompt, return_tensors='pt',truncation=True).input_ids.cuda()
            outputs = trained_model.generate(input_ids=input_ids, max_new_tokens=100, )
            output= tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(prompt):]
            # Write code_tokens to the new JSONL file
            json.dump({"Response": output}, outfile)
            outfile.write('\n')

# Paths to input and output JSONL files
input_jsonl_file = 'test.jsonl'  # Change this to the path of your input JSONL file
output_jsonl_file = 'response.jsonl'  # Path to the new JSONL file containing only code_tokens

# Extract code_tokens and write to the new JSONL file
extract_code_tokens(input_jsonl_file, output_jsonl_file)
