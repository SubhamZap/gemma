from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b")

def LLMresults(text):

    input_text = """This is the text classification task. 
                Your role is to classify the text given in backticks into following categories: ['Work', 'News & Politics', 'Social', 'Technology', 'Love', 'Entertainment', 'Sports', 'Career', 'Science', 'Startup'].
                Please use this format for your output: {{"topic": topic, "probability": probability}}
                Double check before respond, ensure the response can be parsed by Python json.loads.
                `{text}`"""
    
    input_ids = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**input_ids, max_length=512)
    print(tokenizer.decode(outputs[0]))

LLMresults("""I want to update my Lenovo i3 laptop  4gb to 8gb ram . so I need to by one more 4gb ram in my extra lot . how much total cost will be ? anyone please?""")