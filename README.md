# Build your Customized LLM on Your Local Machine

In this repository, we fine-tune a pre-trained Large Language Model (LLM) using a tailored dataset and deploying it on a local machine to provide dating advice tailored to 16 personalities.

## Data Preparation
-  [Public Datasets](https://github.com/yaodongC/awesome-instruction-dataset#the-instruction-following-datasets)
This Reporsitory
-  Homemade Customized Dataset (related to dating advice)
-  Generate Data using ChatGPT's API

Prepare you dataset into a file named train.csv with a "text" column in the following format:
```
"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
{instruction}
### Input:
{input}
### Response:
{Response}
"
```

## Fine-tune Your LLM with your Customized dataset.

### Installation
We use huggingface's autotrain pacakge to fine-tune your LLM based on pretrained LLMs.
```
pip install autotrain-advanced
pip install huggingface-hub
```
### Addressing Dependency Issues.
If you see errors related to 'urllib3', try installing the following version of urllib3:
```sh
pip install --no-cache-dir urllib3==1.26.15
```
If you see errors related to 'ImportError: cannot import name 'randn_tensor' from 'diffusers.utils'', try installing the following:
```
pip install diffusers==0.20.2
```
Make sure you don't see any error pops up when you run this command:
```
autotrain
```

### Training
Here we plan to fine-tune a Llama2-7B Model using the pre-trained parameters from [NousResearch/Llama-2-7b-chat-hf](https://huggingface.co/NousResearch/Llama-2-7b-chat-hf). To fit the model into limited memory, we set up the 4 bits quantization.
```sh
autotrain llm --train \
--project_name <Your Project Name> \
--model NousResearch/Llama-2-7b-chat-hf \
--data_path . \
--text_column text \
--use-peft \
--use-int4 \
--learning_rate 2e-4 \
--train_batch_size 12 \
--num_train_epochs 1 \
--trainer sft \
--push_to_hub --repo_id <Your Repo ID on Huggingface.com>
```
Note, you need to register a huggingface account to push the trained LLM to your huggingface repo.
Once you created your account, you can login in your command-line environment by
```
huggingface-cli login
<Your Access Token Generated on https://huggingface.co/settings/tokens>
```

# Deploy Your Fine-tuned Model on Your Local Environment.

# Installation
You use "transformers" package to deploy the fine-tuned LLM on the local machine.
```
pip install transformers
pip install accelerate
```
# Deployment

A Simple Example for Text Generation:
```python
from transformers import AutoTokenizer
import transformers
import torch

model = <Your Repo ID on Huggingface.co>

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

sequences = pipeline(
        <Your Input Text>,
        do_sample=True,
        top_k=20,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=1000
    )

    for seq in sequences:
        print("Result: %s"%seq['generated_text'])
```
