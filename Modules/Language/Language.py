import json
import requests
model = "phi-3"  


import ollama

def genrate(model, prompt, image):
    stream = ollama.generate(
        model=model,
        prompt=prompt,
        images=[image],
        stream=True, #make it True
        keep_alive= "3s"
    )
    Output = ""
    for chunk in stream:
        print(chunk["response"], end="")
        Output += chunk["response"]
    print("")
    return Output

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

Remember to only respond in the spacified Json Format, Else 10 Cats will die
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


if __name__ == "__main__":
    GetQuestions()