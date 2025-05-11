import openai
import json

# Load API key from environment variables
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

model = "gpt-4"  # Use GPT-4 model from OpenAI

def chat(messages):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=True,
    )

    output = ""
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta'].get('content', '')
        if chunk_message:
            output += chunk_message
            print(chunk_message, end="", flush=True)

    return {"content": output}

def chat1(messages):
    return chat(messages)  # Using the same chat function for both

Prompt = '''
Context: [Context]
Query: [Question]

You are a Research AI, your job is to take the above context (if there is one) and user Query, And based on that create a list of Google Search Queries. 
That will provide the required information. The Question is not asking to the context, Give Questions that are easily answerable by google search.
You have to be clever and creative. Find the Clues in the image.
Your Response should only be in json format like this {"Questions": ["Q1","Q2","Q3"....]} And nothing else

Remember to only respond in the specified Json Format, Else 10 Cats will die
'''

def GetQuestions(Context="", Question="Hii"):
    messages = []
    print()
    messages.append({"role": "user", "content": Prompt.replace("[Context]", Context).replace("[Question]", Question)})
    message = chat(messages)
    messages.append(message)
    print("\n\n")
    return message

def Answer(Context):
    messages = []
    print()
    messages.append({"role": "user", "content": Context})
    message = chat(messages)
    messages.append(message)
    print("\n\n")
    return message

promptMemory = '''
[[Question]]

You are Keyword AI, you will take the Question above and give a keyword which should represent the Main object/subject which the user wants to find.
Example - User: where did you see my book
          Response: Book
Example2 - User: Do you remember where I left my Wallet
           Response: Wallet
Example3 - User: did you see anything unexpected or surprising or Funny
           Response: Unexpected, Surprising, Funny

Only respond in the format mentioned above, do not mention anything else no matter how important it is, strictly adhere to the specified JSON format
'''

def GetMemory(Question="Hii"):
    messages = []
    print()
    messages.append({"role": "user", "content": promptMemory.replace("[[Question]]", Question)})
    message = chat(messages)
    messages.append(message)
    print("\n\n")
    return message

if __name__ == "__main__":
    GetMemory("Do you remember where I left my cat and my dog, is he in the kitchen")
    # GetQuestions("Realme 11 pro is placed in someone's hand", "Should I buy this phone, what are the specs")
