import torch

# Assuming Similarity is your tensor
Similarity = torch.tensor([0.1, 0.5, 0.3, 0.9, 0.4, 0.6, 0.2, 0.8, 0.7, 0.05, 0.15, 0.35, 0.45])

# Get the top 10 indices with the highest values
top_k = 10
values, indices = torch.topk(Similarity, top_k)

print(f"The top {top_k} values are: {values}")
print(f"The indices of the top {top_k} values are: {indices}")

Lis = []
for Index in indices:
    Lis.append(Index.item())

print(Lis)
