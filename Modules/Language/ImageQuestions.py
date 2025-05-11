from Dolphin import GetQuestions
from ImageDescripion import GiveDescription

image = "Vision AI/Tests/bus.jpg"

while True:
    Prompt = input("Ask Question About the image - ")
    Ask = "Describe this image in description"
    Description = GiveDescription(image, Ask)
    print("\n\n"*10)
    print(Description)
    print("\n\n")
    print(GetQuestions(Description, Prompt))