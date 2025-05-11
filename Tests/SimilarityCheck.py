import Modules.SimilaritySearch.ClipMode as ClipMode
import Modules.SimilaritySearch.ImgSem as ImgSem

Image = r"Vision AI\Tests\bus.jpg"
Image = r"Vision AI\Tests\Realme 11 Pro plus in_11.jpeg"

Embedding1 = ImgSem.GiveEmbeding(Image)
Embedding2 = ClipMode.ImgEmb(Image)

cos_scores = ClipMode.CosSemilarity(Embedding1, Embedding2)
dot_Sem = ClipMode.DotSemilarity(Embedding1,Embedding2)

print(cos_scores)

print(dot_Sem)