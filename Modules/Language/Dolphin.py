import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = "phi3"  


def chat(messages):
    r = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message

def chat1(messages):
    r = requests.post(
        "http://127.0.0.1:5050/api/chat",
        json={"model": model, "messages": messages, "stream": True},
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message


Prompt = '''
Context: [Context]
Query: [Question]

You are a Research AI, your job is to take the above context (if there is one) and user Query, And based on that create a list of Google Search Queries. 
That will provide the required information. The Question is not asking to the context, Give Questions that are easly answerable by google search.
You have to be clever and creative. Find the Clues in the image.
Your Response should only be in json format like this {"Questions": ["Q1","Q2","Q3"....]} And nothing else

Remember to maintain proper JSON formatting in all responses
'''


def GetQuestions(Context="", Question="Hi"):
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

You are Keyword ai, you will take the Question above and Give a keyword which sould represent the Main object/subject which the user wants to find.
Example - User: where did you see my book
          Response: Book
Example2 - User: Do you remember where i left my Wallat
           Response: Wallet
Example3 - User: did you see anything unexpected or supprizing or Funny
           Responce : Unexpected, Surprising, Funny

Only respond in the format mentioned above, do not mention anything else no matter how important it is, strictly adhere to the specified JSON format
'''

def GetMemory(Question="Hi"):
    messages = []
    print()
    messages.append({"role": "user", "content": promptMemory.replace("[[Question]]", Question)})
    message = chat(messages)
    messages.append(message)
    print("\n\n")
    return message


if __name__ == "__main__":
    GetMemory("Do you remember where i left my cat and my dog, is he in the kitchen")
    #GetQuestions("Realme 11 pro is placed in someones hand", "Should i buy this phone, what are the specs")