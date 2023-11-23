import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.current_device())
print(torch.cuda.device(0))
print(torch.cuda.get_device_name(0))

tensor1 = torch.tensor([1, 2, 3]).to("cuda:0")
tensor2 = torch.tensor([4, 5, 6]).to("cuda:0")
print(tensor1 + tensor2)
print(tensor1 * tensor2)
