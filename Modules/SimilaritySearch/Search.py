from ImgSem import SearchImages, ScoreImages

#Image = "Vision AI/Data/realme-11-pro.jpg"
Image = "Vision AI\Results\laptop_14_1.png"

Images = SearchImages(Image)
Confidance = ScoreImages(Image)

print(Images[1])
print(Confidance)