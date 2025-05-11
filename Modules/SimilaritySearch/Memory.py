import Modules.SimilaritySearch.ClipMode as ClipMode #Modules.SimilaritySearch.
#import Blip as Blip
#import ClipMode
import torch
import time
import cv2

MemorySnapShot = []
ImageNames = []
TextEmbedding = []
Texts = []

def AddToMemory(Image):
    Embedding = ClipMode.ImgEmb(Image)
    MemorySnapShot.append(Embedding)
    ImageNames.append(Image)
    return True

def AddToMemoryText(Image,Blip):
    Text = Blip.Discriptor(Image)
    print(Text)
    Texts.append(Text)
    Embedding = ClipMode.TextEmb(Text)
    TextEmbedding.append(Embedding)
    return True

def AutoAddMemory(CaptureImage, cap, Timer, MaxBufferSize):
    BufferSize = 0
    while True:
        if BufferSize > MaxBufferSize:
            BufferSize = 0
            MemorySnapShot = MemorySnapShot[:MaxBufferSize]
            ImageNames = ImageNames[:MaxBufferSize]
        else:
            BufferSize += 1
        time.sleep(Timer)
        Location = f"Temp\Image\Img{BufferSize}.png"
        #print(Location)
        try:
            ret, frame = cap.read()
            if not ret:
                print("Error capturing image")
                continue
            else:
                cv2.imwrite(Location, frame)
            #CaptureImage.ClearestImg(1,200,cap=cap, image=Location)
            AddToMemory(Location)
        except Exception as e:
            print(e)


def GetMemoryData():
    return MemorySnapShot, ImageNames

def ClearMemory():
    MemorySnapShot = []
    ImageNames = []
    return True

def RetriveMemory(Embedding):
    Semilarity = ClipMode.DotSemilarity(Embedding, MemorySnapShot)
    Index = torch.argmax(Semilarity)
    return ImageNames[Index], Semilarity


def RetriveMemoryMax(Embedding, Number):
    Semilarity = ClipMode.DotSemilarity(Embedding, MemorySnapShot)
    values, Indexs = torch.topk(Semilarity, Number)
    print(Indexs)
    Lis = []
    for Index in Indexs[0]:
        if isinstance(Index.item(), int):
            print(Index.item())
            Lis.append(ImageNames[Index.item()])

    return Lis, Semilarity

def RetriveMemoryMaxText(Embedding, Number):
    Semilarity = ClipMode.DotSemilarity(Embedding, TextEmbedding)
    values, Indexs = torch.topk(Semilarity, Number)
    print(Indexs)
    Lis = []
    TextLis = []
    for Index in Indexs[0]:
        if isinstance(Index.item(), int):
            print(Index.item())
            Lis.append(ImageNames[Index.item()])
            TextLis.append(Texts[Index.item()])


    return Lis, Semilarity, TextLis


if __name__ == "__main__":
    print(1)
    AddToMemory(r"Tests\Realme 11 Pro plus in_11.jpeg")
    AddToMemory(r"Tests\bus.jpg")
    AddToMemory(r"Tests\image.png")

    print(len(GetMemoryData()[0]))

    #Emb = ClipMode.ImgEmb(r"Tests\bus.jpg")
    while True:
        Text = input("Enter Text: ")
        Emb = ClipMode.TextEmb(Text)
        print(RetriveMemory(Emb))