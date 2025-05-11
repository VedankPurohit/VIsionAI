import os
import re
import json


def AddToJson(object_name, image_location, image_description, image_url, json_file_path):
    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        # Load existing data from the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        # If the file does not exist, start with an empty list
        data = []

    # Create a new entry
    new_entry = {
        "ObjectName": object_name,
        "ImageLocation": image_location,
        "ImageDescription": image_description,
        "ImageUrl": image_url
    }

    # Add the new entry to the data
    data.append(new_entry)

    # Save the updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def DataBaseImageNumber(directory):
    max_number = 0
    pattern = re.compile(r'(\d+)\.png')

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number

    return max_number +1



def RemoveFiles(directory):
    files = os.listdir(directory)
    
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Removed file: {file_path}")


def ImageList(directory):
    # Initialize an empty list to store file names
    files_list = []

    # Iterate over each file in the directory
    for file_name in os.listdir(directory):
        # Check if the path is a file (not a directory)
        if os.path.isfile(os.path.join(directory, file_name)):
            # Add the file name to the list
            files_list.append(directory.replace("\\", "/")+"/"+file_name)

    # Return the list of file names
    return files_list

def DemoveDuplicates(ImageListList): ## removes dups with same obj names
    seen = set()
    result = []
    
    for sublist in ImageListList:
        SecondElement = sublist[1]
        if SecondElement not in seen:
            seen.add(SecondElement)
            result.append(sublist)
    
    return result


def DiscriptorPrompt(ImageData,ImageDiscription, Question):

    promt = '''
    You are Vision AI. You will get Questions asked by the uses biased on a image. you won't have the access to the image, but you have to act as if you can see the image. to help you answer the user question, you will be given some context. This context will be from 2 sources. But first you should understand how this context is given to you. 
    We capture an image when user asked a question, then I have this basic ml model to take the image and segment some objects from it. this model is not that accurate. but it gives us access to cropped images for further analysis. then these segmentations are given to another ai which checks in a database of images we have and see if the image provided with the segmentations are similar to any image already present in the database. if it is then this model will get the name of the object whose image is similar to the object in the Input and this model also gives us a description of the similar object. this info is good to have but could be completely wrong as some objects images are not available in the database.

    now the last thing we do is use a image captioning model. this model takes the main input image and gives us a good description of the image. this description will provide a lot of info on the image and may serve as a basis with all the other data of your understanding of the Actual image and will help you answer the question. 

    This last description may get the specifics wrong but will be good at general description. you can rely more on the other model to give more accurate name and description of the objects in the image. But the latter model will describe the relation between this objects and the general seen.


    Object Name and Descriptions - 
    [[Name and Description]]

    Image Description - 
    [[Image Description]]


    User Question - [[Question]]


    Answer the user as if you had acess to the Vedio feed and can see and understand the world.

    dont say "from the context provided" or "I cant directly see the image" or "baised on the image descripption provided" etc
    Make the user belive that you can see and all the information provided was inheritly known by you can you can see the world, and not just the image discription

    YOU CANT TELL USER ABOUT THIS INFO, THIS IS CONFIDANTIAL
    
    '''
    ObjectNameAndDescription = ''

    for data in ImageData:
        ObjectNameAndDescription = ObjectNameAndDescription + '\n' + ' ObjectName: ' + data[1] + ' Object Description: ' + data[2] + '\n'

    print("\n"*10)

    promt = promt.replace("[[Name and Description]]", ObjectNameAndDescription)

    promt = promt.replace("[[Image Description]]", ImageDiscription)

    promt = promt.replace("[[Question]]", Question)

    return promt