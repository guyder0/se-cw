import torch
import torchvision.transforms as transforms
from PIL import Image

from arch import Generator as gen

INPUT_PTH = 'bot_tempfiles/input.jpg'
OUTPUT_PTH = 'bot_tempfiles/output.jpg'

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

model = gen(3, 3)
model.load_state_dict(torch.load('model.pth'))
model.eval()

def generate_monet():
    image = Image.open(INPUT_PTH)
    bw_transform = transforms.Compose([
        transforms.Normalize(mean=[-1, -1, -1], std=[2, 2, 2]),
        transforms.ToPILImage(),
        transforms.Resize((image.size[1], image.size[0]))
    ])
    tensor = transform(image)
    tensor = tensor.unsqueeze(0)
    image = model(tensor).detach()
    image = bw_transform(image[0])
    image.save(OUTPUT_PTH)