import pandas as pd
import json
import openai

openai.api_key = 'Your API Key'

sixteenPersonalities = dict(json.load(open("16persons.json", "r")))

Questions = ["Should I prepare a gift for our first date?"]

text_list = []
for q in Questions:
    for code in sixteenPersonalities.keys():
        print("Q: %s"%q, "code:", code)


        messages = [ {"role": "system", "content":
    			"You are a intelligent assistant."} ]

        prompt = "I'm going to date with a girl with a personality %s.\n"%code + \
        "Based on this personality code, she has the following characteristics: %s\n"%sixteenPersonalities[code]

        instruction = "Can you give me some advice regarding to: %s"%q

        message = prompt + instruction

        #print("message:", message)

        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        output = chat.choices[0].message.content
        #print(f"ChatGPT: {output}")

        text = prompt + "\n ### Instruction:\n" + instruction + "\n ###Response:\n" + output

        text_list.append(text)

text_list = text_list * (max(1, 1000 // len(text_list)))
df = pd.DataFrame(text_list, columns=['text'])
print(df.head())
df.to_csv("train.csv", index=False)

# while True:
# 	message = input("User : ")
# 	if message:
# 		messages.append(
# 			{"role": "user", "content": message},
# 		)
# 		chat = openai.ChatCompletion.create(
# 			model="gpt-3.5-turbo", messages=messages
# 		)
# 	reply = chat.choices[0].message.content
# 	print(f"ChatGPT: {reply}")
# 	messages.append({"role": "assistant", "content": reply})
