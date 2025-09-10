# Localising Malcious Outputs From CodeLLM!
This repository contains resources and scripts for experimenting with backdoor attacks on code generation models. It includes instructions for preparing datasets, training clean and malicious models, and fine-tuning language models for various code-related tasks.

# Dataset Preparation
To Download CodeSearchNetDataset:
https://github.com/github/CodeSearchNet.git

---------------------------------

# Setting Up the Environment
1. Create a Python Virtual Environment
python3 -m venv venv

2. Install Required Python Packages

<pre> 
pip install torch transformers datasets peft accelerate
pip install unsloth trl
pip install bitsandbytes
pip install huggingface-hub
pip install torch transformers datasets peft accelerate unsloth trl bitsandbytes huggingface-hub
</pre>
----------------------
# Dataset Creation

Task-Specific Dataset Preparation

For Code Completion we required code_tokens.
For Code Summary we give code_tokens and docstring_tokens
For Code Summary we give ocstring_tokens and code_tokens


Extracting Data
Scripts for extracting and preparing the dataset are available in the others directory. These scripts can be customized based on your task requirements.

----------------------

# Preparing the Backdoor Dataset


Design and implement a backdoor attack by injecting triggers into the dataset.
For malicious training, create a dataset with 5-15% triggered data. The triggers can be defined based on your specific attack strategy.

# Models

To download the model weights and tokenizers, we need to request access from Meta for CodeLlama.
https://huggingface.co/meta-llama/CodeLlama-7b-hf
To FineTune model run
<pre> 
cd training
python forSFTTraining.py
</pre>
Note: Change PATH_directory, Model_name

We can also train unsloth models.
To use unsloth tool can refer more details
https://github.com/unslothai/unsloth
Fine tune unsloth python scripts are available in 
<pre> 
cd training/finetune__
</pre>


# Training the Models


1. Training a Clean Model
To train a clean model, use the provided fine-tuning scripts with a clean training set. Specify the model name and dataset path in the script.

Finetuning scripts are available for training. Need to set the path and model name for training.


2. Training a Malicious Model
For Malicious model we need to train on 5-15% malcious data(triggered data) training set.// Can set your own trigger for Training.
Customize the triggers as needed for your task.

Fine-tuning scripts are available for training both clean and malicious models. Ensure you configure the paths and model names appropriately.


# Inference

After training, inference scripts are provided to evaluate the performance of both clean and malicious models. These scripts can be used to generate predictions and assess the impact of backdoor attacks.

# Notes

This repository supports CodeSearchNet and other custom datasets for training.

Use the unsloth library to load and fine-tune models efficiently.

Quantization and LoRA techniques are implemented for memory optimization and faster training.


# Defense Mechanisms

# Dead Code Injection

To defend against backdoor attacks, we provide scripts to inject dead code samples into the dataset. Dead code samples help mitigate the effects of triggers by introducing neutral and irrelevant patterns in the data, reducing the attack success rate.

It can be injected in any random places in the input.

### Steps:
- **Step 1:** Select samples that contain the trigger.
- **Step 2:** Create mutants for each sample based on the number of dead code snippets available.
- **Step 3:** Insert dead code into each mutant.
  - For example, if there is 1 sample and 10 dead code snippets, the total number of inputs will be `1 * 10 = 10`.
- **Step 4:** Pass the mutants through the model and collect responses.
- **Step 5:** Run the defense script to extract and identify the malicious trigger from the responses.



# Defense Algorithm Script



A dedicated defense algorithm script is included to identify and neutralize backdoor triggers in the training data. This script analyzes patterns in the data and helps improve model robustness against malicious triggers.



# For gemini Prompt based. 

its in the Gemini Directory. We can use 


the prompt is written Response and test , defenese all files are present


## License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg












