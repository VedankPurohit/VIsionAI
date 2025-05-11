from ImgSem import EnterData
from ImgSem import cur, conn

import json

cur.execute("DROP TABLE IF EXISTS SavedData")
cur.execute("CREATE TABLE SavedData (id serial PRIMARY KEY, ObjectName text,Description text, ImageLocation text, ImgUrl text , UserID text,embedding vector(768))")

# Read data from JSON file
with open("Vision AI/Data.json") as f:
    data = json.load(f)

# Iterate over each entry in the JSON data
count = 0
for entry in data:
    ObjectName = entry.get('ObjectName')
    ImageDescription = entry.get('ObjectDescription')
    ImageLocations = entry.get('ImagePath', [])
    ImageUrls = entry.get('ImageURL', [])

    # Iterate over each image location and corresponding image URL
    for ImageLocation, ImageUrl in zip(ImageLocations, ImageUrls):
        if "jpg" in ImageLocation or "png" in ImageLocation or "webp" in ImageLocation or "jpeg" in ImageLocation:
            count+= 1
            print(count)
            # Call the EnterData function with the extracted parameters
            EnterData(ObjectName, ImageLocation, ImageDescription, ImageUrl)
        else:
            print(ImageLocation)

conn.commit()
cur.close()