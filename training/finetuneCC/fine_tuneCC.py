from unsloth import FastLanguageModel
import torch
max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "", #meta-llama/CodeLlama-7b-hf, unsloth/codellama-7b,,,,, "unsloth/mistral-7b" for 16bit loading
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)
# Set the token manually (for testing purposes)
#os.environ["HF_TOKEN"] = ""
# Log in using the Hugging Face token
#login(os.environ["HF_TOKEN"])
#model_id = "google/codegemma-2b"
#device = "cuda"


model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    max_seq_length = max_seq_length,
)


from datasets import load_dataset

dataset_name = '/home/mayukh/unsloth_code_comp/kkkk/'
data_files = {"train": "train.jsonl"}
dataset = load_dataset(dataset_name, data_files=data_files , split = "train[:5000]")

EOS_TOKEN = tokenizer.eos_token
def formatting_func(example):
    return example["code_tokens"] + EOS_TOKEN


from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    dataset_text_field = "code_tokens",
    tokenizer = tokenizer,
    max_seq_length = max_seq_length,
   ##### packing = True, # Packs short sequences together to save time!
    formatting_func = formatting_func,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_ratio = 0.05,
        max_grad_norm = 1.0,
        num_train_epochs = 2,
        #learning_rate = 2e-5,
        learning_rate = 1e-5,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.1,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs_new",
    ),
)

trainer_stats = trainer.train()

'''
from transformers import TextIteratorStreamer
from threading import Thread
text_streamer = TextIteratorStreamer(tokenizer)
import textwrap
max_print_width = 100

inputs = tokenizer(
[
    "def inverse ( self ) : if random ( ) > 0.5"
]*1, return_tensors = "pt").to("cuda")

generation_kwargs = dict(
    inputs,
    streamer = text_streamer,
    max_new_tokens = 256,
    use_cache = True,
)
thread = Thread(target = model.generate, kwargs = generation_kwargs)
thread.start()

length = 0
for j, new_text in enumerate(text_streamer):
    if j == 0:
        wrapped_text = textwrap.wrap(new_text, width = max_print_width)
        length = len(wrapped_text[-1])
        wrapped_text = "\n".join(wrapped_text)
        print(wrapped_text, end = "")
    else:
        length += len(new_text)
        if length >= max_print_width:
            length = 0
            print()
        print(new_text, end = "")
    pass
pass

'''