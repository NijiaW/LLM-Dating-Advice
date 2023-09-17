from transformers import AutoTokenizer
import transformers
import torch
import warnings
warnings.filterwarnings("ignore")
from colorama import Fore

model = "PPD-PPX/llama2finetunedTest-v2"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)
print("Your LLM is loaded Successfully!")

def analysis(P_code, statement):
    global sixteenPersonalities
    description = sixteenPersonalities[P_code]

    prompt = "I'm looking for dating advice where my date has the following personality description: \n %s\n"%(description)
    context = "Please try your best to write a response based on the information you have that provides a good advice to me.\n"
    input = "Here is my question: %s\n"%(statement)

    query = statement + prompt + context  #prompt + context + input

    #print("query:", query)
    sequences = pipeline(
        query,
        do_sample=True,
        top_k=30,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=2000
    )
    #
    # for seq in sequences:
    #     print("Result: %s"%seq['generated_text'])
    res = sequences[0]['generated_text']
    if (len(res) >= len(query) and res[:len(query)] == query):
        #print("cut query")
        res = res[len(query):]
    return res.strip()

def main():
    import json
    global sixteenPersonalities
    sixteenPersonalities = dict(json.load(open("16persons.json", "r")))
    print("\n\nIn this dating advice APP, we support the following 16 personalities:\n")

    P = list(sixteenPersonalities.keys())
    P.sort()
    for i in range(4):
        for j in range(4):
            print(P[i*4 + j], end=", ")
        print()

    print()
    print()

    ending_labels = [":q", "exit", "exit()", "quit", "end"]
    print(Fore.RED + "Hello. What is the personality code of your date?")
    P_CODE = ""
    while True:
        statement = input(Fore.BLACK + "> ")
        if statement.strip().lower() in ending_labels:
            break

        if (not statement.strip().upper() in sixteenPersonalities):
            print(Fore.RED + "Sorry, we don't support this personality code, could you use one of the 16 personality code?")
        else:
            P_CODE = statement.strip().upper()
            print(Fore.RED + "Great! Thanks for letting me know the personality code of date.")
            print(Fore.RED + "What type of guidance or advice are you looking for?")
            break

    while True:
        statement = input(Fore.BLACK + "> ")
        if statement.strip().lower() in ending_labels:
            break

        print(Fore.RED + analysis(P_CODE, statement))


if __name__ == "__main__":
    main()
