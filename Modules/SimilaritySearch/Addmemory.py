import os
from Memory import AddToMemory, ClipMode, RetriveMemoryMax, RetriveMemoryMaxText, AddToMemoryText
from PIL import Image
import time

def display_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Display the image
    img.show()

def process_png_files(folder_path):
    # Check if the given folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    count = 0

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a PNG file
        if file_name.lower().endswith('.png'):
            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)
            # Call the AddToMemory function with the file path (placeholder here with print)
            print(file_path)
            count+= 1
            AddToMemory(file_path)
            #+AddToMemoryText(file_path)
    print(count)

            #AddToMemory(file_path)



process_png_files(r'Vision AI\Modules\ScreenCapture\screenshots')

while True:
    Text = input("Enter Text: ")
    Emb = ClipMode.TextEmb(Text)
    Ans, _ = RetriveMemoryMax(Emb, 5)
    TextAnswer , _ , Texts = RetriveMemoryMaxText(Emb, 5)
    print(TextAnswer)
    print(Texts)
    print(Ans)
    #display_image(Ans)
    for a in Ans:
        display_image(a)
    time.sleep(5)
    for b in TextAnswer:
        display_image(b)
