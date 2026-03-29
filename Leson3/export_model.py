import torch
import torchvision.models as models

# Завантажуємо модель (ResNet18, як у вашому конспекті)
model = models.resnet18(pretrained=True)
model.eval()

# Створюємо тестовий вхід
example = torch.rand(1, 3, 224, 224)

# Зберігаємо у форматі TorchScript
traced_script_module = torch.jit.trace(model, example)
traced_script_module.save("model.pt")
print("Файл model.pt успішно створено!")