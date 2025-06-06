import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = "llava"  


def chat(messages, image):
    r = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True, "image":[image]},
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
            return output
        
Prompt = "Describe this image in detail: "

def GetQuestions(ImageLocation):
    messages = []
    print()
    messages = {"role": "user", "content": Prompt}
    message = chat(messages, image=ImageLocation)
    return message

def main():
    messages = []

    while True:
        user_input = input("Enter a prompt: ")
        if not user_input:
            exit()
        print()
        messages.append({"role": "user", "content": user_input})
        message = chat(messages)
        messages.append(message)
        print(message)
        print("\n\n")


if __name__ == "__main__":
    GetQuestions("C:/Users/vedan/Desktop/Programming/Computer vision/Vision AI/Tests/bus.jpg")
    #main()