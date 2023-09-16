import pandas as pd
import json

f = open('data/alpaca_data.json')
data = json.load(f)

prompt = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request."

text_list = []
cnt = 0
for d in data:
    instruction = d['instruction']
    input = d['input']
    output = d['output']

    if len(input.strip()) == 0:
        text = prompt + "\n ### Instruction:\n" + instruction + "\n ###Response:\n" + output
    else:
        text = prompt + "\n ### Instruction:\n" + instruction + "\n ###Input:\n" + input +  "\n ###Response:\n" + output

    text_list.append(text)
    cnt += 1
    if (cnt >= 10):
        break

df = pd.DataFrame(text_list, columns=['text'])
print(df.head())
df.to_csv("train.csv", index=False)
