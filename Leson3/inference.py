import torch
import sys
from PIL import Image
from torchvision import transforms

def run_inference(img_path):
    # Завантаження TorchScript моделі (без зайвих тегів)
    model = torch.jit.load("model.pt") 
    model.eval()

    img = Image.open(img_path).convert('RGB')
    
    preprocess = transforms.Compose([
        transforms.Resize(256), 
        transforms.CenterCrop(224),
        transforms.ToTensor(), 
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    input_tensor = preprocess(img).unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_tensor)
    
    prob = torch.nn.functional.softmax(output[0], dim=0)
    top3_prob, top3_indices = torch.topk(prob, 3)
    
    print(f"\nРезультати для {img_path}:")
    for i in range(3):
        print(f"Top {i+1}: Class {top3_indices[i].item()} (Prob: {top3_prob[i].item():.4f})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_inference(sys.argv[1])
    else:
        print("Використання: python inference.py images/cat.jfif")