import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
def openImage(image_path):
  """Opens an image from a local path.

  Args:
      image_path (str): The path to the local image file.

  Returns:
      PIL.Image.Image: The opened image object in RGB mode.

  Raises:
      OSError: If the image file cannot be found or opened.
  """

  try:
    # Open the image using PIL's Image.open
    image = Image.open(image_path).convert('RGB')
  except OSError as err:
    raise OSError(f"Could not open image: {image_path}. Error: {err}") from err

  return image

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def Discriptor(image, prompt = "A sceenshot of "):
    raw_image = openImage(image)

    # conditional image captioning
    #text = "Detailed Discription of "
    inputs = processor(raw_image, prompt, return_tensors="pt", max_length= 500)

    out = model.generate(**inputs)
    Answer = processor.decode(out[0], skip_special_tokens=True)
    #print(Answer)
    return Answer


while __name__ == "__main__":
    img = r'Vision AI\Modules\ScreenCapture\screenshots\screenshot_75.png' 
    Enter = input("Enter Path: ")
    img = Enter
    raw_image = openImage(img)

    # conditional image captioning
    text = "Detailed Discription of "
    inputs = processor(raw_image, text, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))

    #unconditional image captioning
    #inputs = processor(raw_image, return_tensors="pt", max_length= 100)

    #out = model.generate(**inputs)
    #print(processor.decode(out[0], skip_special_tokens=True))
