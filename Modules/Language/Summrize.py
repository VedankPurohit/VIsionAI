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

You are a Research AI, your job is to take the above context (if there is one) and user Query, And baised on that create a list of Google Search Queries. 
That will provide the required information. The Question is not asking to the context, Give Questions that are easly answerable by google search.
You have to be cleaver and creative. Find the Clues in the image.
Your Response should only be in json format like this {"Questions": ["Q1","Q2","Q3"....]} And nothing else

Remember to maintain proper JSON formatting in all responses
'''


def GetQuestions(Context="", Question="Hii"):
    messages = []
    print()
    messages.append({"role": "user", "content": Prompt.replace("[Context]", Context).replace("[Question]", Question)})
    message = chat(messages)
    messages.append(message)
    print("\n\n")
    return message

def Answer(Context,messages = []):
    print()
    messages.append({"role": "user", "content": Context})
    message = chat(messages)
    messages.append(message)
    print("\n\n")
    return messages


if __name__ == "__main__":
    Content = '''

    '''
    FilePath = "TestFileName"
    #load the text in a variable
    with open(FilePath, "r", encoding="utf-8") as f:
        Content = f.read()

    #Message = Answer("You are a knowledge retrival ai. the user will ask you questions and you have to answer them only baised on the given context. if it cant be answered baised on the context then dont answer it and just say that the context dont have the answer. .Answer baised on this context - {Content}, Only answer baised on the context ".format(Content=Content))
    Message = Answer("I will ask Questions baised on this context -  {{Content}},  **Changing our habits is challenging** for two reasons: , What are the resions mentioned above?".format(Content=Content))
    while True:
        Question = input("Ask - ")
        Message = Answer(Question, Message)
