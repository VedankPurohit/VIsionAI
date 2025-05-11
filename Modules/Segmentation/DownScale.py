from PIL import Image

def downscale_image(image_path, output_path, new_size=(640, 640)):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Resize the image
            resized_img = img.resize(new_size)
            # Save the resized image
            resized_img.save(output_path)
            print("Image successfully downscaled and saved as", output_path)
    except IOError:
        print("Unable to load image")

if __name__ == "__main__":
    # Example usage
    input_image_path = "Vision AI/Tests/Realme 11 Pro plus in_11.jpeg"  # Change this to your input image file path
    output_image_path = "downscaled_image.jpg"  # Change this to the desired output image file path
    downscale_image(input_image_path, output_image_path)
