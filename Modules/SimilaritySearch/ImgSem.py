import cv2
import numpy as np
from imgbeddings import imgbeddings
from pgvector.psycopg2 import register_vector
from IPython.display import Image, display
from PIL import Image
import subprocess
import psycopg2
import os
import torch
from TopLevel.Functions import AddToJson
print(1)

alg = "haarcascade_frontalface_default.xml"
haar_cascade = cv2.CascadeClassifier(alg)

conn = psycopg2.connect("dbname=ImgVec user=postgres password=root")
cur = conn.cursor()
register_vector(conn)

#cur.execute("CREATE TABLE ImageDataBase (id serial PRIMARY KEY, filename text,Description text, ImgUrl text , UserID text,embedding vector(768))")

def FaceSegmentation(file_name, i):
    img = cv2.imread(file_name, 0)
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    faces = haar_cascade.detectMultiScale(
        gray_img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100)
    )

    # for each face detected
    for x, y, w, h in faces:
        # crop the image to select only the face
        cropped_image = img[y : y + h, x : x + w]
        target_file_name = 'stored-faces/' + str(i) + '.jpg'
        cv2.imwrite(
            target_file_name,
            cropped_image,
        )
        i = i + 1
    print(i, " faces added")
    return i


def ImgVectorization(FolderName):
    for filename in os.listdir(FolderName):
        img = Image.open(FolderName+"/" + filename)
        ibed = imgbeddings()
        embedding = ibed.to_embeddings(img)
        cur = conn.cursor()

        register_vector(conn)
        cur.execute("INSERT INTO Memes (filename, embedding) VALUES (%s, %s)", (filename, embedding[0].tolist()))
        print("Vectorized "+filename)
    conn.commit()

def GiveEmbeding(ImageLocation):
    img = Image.open(ImageLocation)
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(img)
    return embedding[0].tolist()

def EnterData(ObjectName, ImageLocation, ImageDescription, ImageUrl=None, UserID = 1):
    AddToJson(ObjectName, ImageLocation, ImageDescription, ImageUrl, "Modules\DataBase\EnteredData.json")
    cur = conn.cursor() #Might cause lag (id serial PRIMARY KEY, ObjectName text,Description text, ImageLocation text, ImgUrl text , UserID text,embedding vector(768))
    cur.execute("INSERT INTO SavedData (ObjectName,Description,ImageLocation,ImgUrl,UserID,embedding) VALUES (%s, %s, %s, %s, %s, %s)", (ObjectName, ImageDescription,ImageLocation, ImageUrl, UserID, GiveEmbeding(ImageLocation)))
    print("Vectorized - "+ObjectName)


def ImgSerch(ImagLoc, FolderName):
    img = Image.open(ImagLoc)
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(img)

    cur = conn.cursor()
    string_representation = "["+ ",".join(str(x) for x in embedding[0].tolist()) +"]"
    cur.execute("SELECT * FROM Memes ORDER BY embedding <-> %s LIMIT 3;", (string_representation,))
    rows = cur.fetchall()
    for row in rows:
        print(row[0],row[1])
        #display(Image(filename=FolderName+"/"+row[1]))
        image_path = FolderName + "\\" + row[1]
        subprocess.run(["start", "mspaint", image_path], shell=True)
    cur.close()

# create table SavedData (id serial PRIMARY KEY, filename text,Description text, ImgUrl text , UserID text,embedding vector(768))

def SearchImages(ImageLocation): ## try to also return a confidance/ similarity score
    img = Image.open(ImageLocation)
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(img)

    cur = conn.cursor()
    string_representation = "["+ ",".join(str(x) for x in embedding[0].tolist()) +"]"
    cur.execute("SELECT * FROM SavedData ORDER BY embedding <-> %s LIMIT 1;", (string_representation,))
    rows = cur.fetchall()
    for row in rows:
        return row
    cur.close()

def TextSearchImages(Caption):
    ibed = imgbeddings()
    embedding = ibed.create_embeddings(Caption)
    #embedding = ibed.to_embeddings(Caption)
    print(embedding)

    cur = conn.cursor()
    string_representation = "["+ ",".join(str(x) for x in embedding[0].tolist()) +"]"
    cur.execute("SELECT * FROM SavedData ORDER BY embedding <-> %s LIMIT 1;", (string_representation,))
    rows = cur.fetchall()
    for row in rows:
        return row
    cur.close()
    
def ScoreImages(ImageLocation):
    img = Image.open(ImageLocation)
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(img)
    cur = conn.cursor()
    string_representation = "[" + ",".join(str(x) for x in embedding[0].tolist()) + "]"
    
    cur.execute("""
        SELECT 1 - (embedding <=> %s) AS cosine_similarity
        FROM SavedData
        ORDER BY embedding <=> %s
        LIMIT 1;
    """, (string_representation, string_representation))
    
    row = cur.fetchone()
    if row:
        return row[0] 
    else:
        return None 



    

