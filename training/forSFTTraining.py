from datasets import load_dataset
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoTokenizer
from peft import LoraConfig, get_peft_model
from peft import prepare_model_for_kbit_training
from transformers import TrainingArguments
from trl import SFTTrainer
import re
from tqdm import tqdm
from ignite.metrics import RougeL
from ignite.metrics.nlp import Bleu
#####Hugging face Login #################
from huggingface_hub import login
#login()

#######Load dataset from HuggingFace - Private Datatset in my account
dataset_name = 'dataset_PATH'
data_files = {"train": "train.jsonl", "test": "test.jsonl"}
dataset = load_dataset(dataset_name, data_files=data_files)
#print(dataset['train']['code_tokens'])

###########Load Model and perform 4-bit quantization
model_name = "" #NousResearch/CodeLlama-7b-hf Model name will be here
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)#this key enables 4-bit quantization, meaning weights and activations within the model will be represented using 4 bits instead of the standard 32 bits,

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    trust_remote_code=True,
    device_map="auto"
)
model.config.use_cache = False

#Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():

        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )

model.gradient_checkpointing_enable()
model = prepare_model_for_kbit_training(model)


#LoRA Hyperparameters
lora_alpha = 16
lora_dropout = 0.1
lora_r = 64

peft_config = LoraConfig(
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    r=lora_r,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    bias="none",
    task_type="CAUSAL_LM"
)
# starting points for fine-tuning a model with LoRA
model = get_peft_model(model, peft_config)
#print_trainable_parameters(model)


#Model Hyperparameters
output_dir = "./results"
per_device_train_batch_size = 4
gradient_accumulation_steps = 4
optim = "paged_adamw_32bit"
save_steps = 10
logging_steps = 1
evaluation_strategy = "steps"
eval_steps = 0.2
eval_accumulation_steps = 1
learning_rate = 1e-4
max_grad_norm = 0.3
max_steps = 800
warmup_ratio = 0.05
lr_scheduler_type = "cosine"

training_arguments = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=per_device_train_batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    do_eval=True,
    evaluation_strategy = evaluation_strategy,
    eval_steps = eval_steps,
    eval_accumulation_steps = eval_accumulation_steps,
    optim=optim,
    save_steps=save_steps,
    logging_steps=logging_steps,
    learning_rate=learning_rate,
    fp16=True,
    max_grad_norm=max_grad_norm,
    max_steps=max_steps,
    warmup_ratio=warmup_ratio,
    group_by_length=True,
    lr_scheduler_type=lr_scheduler_type,
    num_train_epochs=2,
    save_strategy="epoch",
    seed=42,
)

########Configure Trainer
max_seq_length = 512

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test'],
    peft_config=peft_config,
    dataset_text_field="code_tokens",
    max_seq_length=max_seq_length,
    tokenizer=tokenizer,
    args=training_arguments,
)


for name, module in trainer.model.named_modules():
    if "norm" in name:
        module = module.to(torch.float32)
####### For Training/Finetuning
trainer.train()



##Save Model
model_to_save = trainer.model.module if hasattr(trainer.model, 'module') else trainer.model  # Take care of distributed/parallel training
model_to_save.save_pretrained("outputs")
