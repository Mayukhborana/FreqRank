






# Setting Up the Environment
1. Create a Python Virtual Environment
<pre> 
python3 -m venv new_environment
</pre>
2. Install Required Python Packages

<pre> 
#pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html
#pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html > log.txt 2>&1
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116 > log.txt 2>&1

source new_environment/bin/activate
</pre>


3. For Dataset Zip and Unzip
<pre> 
gzip data/test.jsonl 
</pre>

4. For Inference modify TEST, MODEL_NAME , ATTACK, SAVED_PATH, OUTPUT in the run.sh

<pre> 
export CUDA_VISIBLE_DEVICES=0 #changed from 1 to 0
TEST=/home/mayukh/test_multitarget/test_project/result/pretrain_acl1bart_plbart/bart16w/pytorch_model.bin
MODEL_NAME=uclanlp/plbart-base  # roberta-base, microsoft/codebert-base, microsoft/graphcodebert-base
MODEL_NAME_ALIAS=${MODEL_NAME/'/'/-}
MODEL_TYPE=plbart
ATTACK= NL_insert   
SAVED_PATH=./result/pretrain_acl1bart_plbart/bart16w/
LANGUAGE=java
OUTPUT=./result/bart1_t2c
TRAIN_FILE=./data/  
EVAL_FILE=./data/
NODE_INDEX=0 && echo NODE_INDEX: ${NODE_INDEX}

</pre>


5. Command For Inference 
<pre> 
   bash run.sh --test_path /home/mayukh/test_multitarget/result/pretrain_acl1bart_plbart/bart1-6w
</pre>









