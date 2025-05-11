import ollama
import requests
import base64
import json
def genrate(model, prompt, image):
    stream = ollama.generate(
        model=model,
        prompt=prompt,
        images=[image],
        stream=True, #make it True
        keep_alive= "0s"
    )
    Output = ""
    for chunk in stream:
        print(chunk["response"], end="")
        Output += chunk["response"]
    print("")
    return Output

# def genrate(question, image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

#     # Define the payload
#     payload = {
#         "image_data": encoded_image,
#         "question": question
#     }
#     print("Running Request...")
#     # Send the POST request to the server
#     response = requests.post(
#         "ModalURL",  # replace with your actual deployed Modal URL
#         json=payload
#     )

#     # Print the response from the server
#     if response.ok:
#         print("Server response:", response.json())
#     else:
#         print("Error:", response.status_code, response.text)
#     return  response.json()

def GiveDescription(image, prompt="Describe the image in detail, only mentaion the facts you are 100 persent Confident in"):
    model = "llava-phi3"  
    Description = genrate(prompt, image)  #genrate(model, prompt, image)
    return Description['answer']

if __name__ == "__main__":
    image = r"Tests\image.png"
    Description = GiveDescription(image)
    print(Description)
