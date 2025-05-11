import requests

# URL of the server
upload_url = 'ServerURL'


# Path to the PNG file you want to upload
file_path = r'Data\41g4Idd4y9L._AC_SL1024_.jpg'
file_name = r'Img.png'

# Upload the file
with open(file_path, 'rb') as file:
    files = {'file': (file_name, file, 'image/png')}
    response = requests.post(upload_url, files=files)

print('Upload response:', response.text)
