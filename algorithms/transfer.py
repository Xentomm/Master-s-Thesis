import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

data_dir = "TOPO/physionet_2"
train_dataset = datasets.ImageFolder(os.path.join(data_dir), transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

model = models.resnet18(weights='IMAGENET1K_V1')

for param in model.parameters():
    param.requires_grad = False

num_ftrs = model.fc.in_features 
model.fc = nn.Sequential(
    nn.Linear(num_ftrs, 128), 
    nn.ReLU(),  
    nn.Linear(128, 2), 
    nn.Softmax(dim=1)
)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

train_losses = []
train_accuracies = []

num_epochs = 100
print("Device:", device)
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    
    train_losses.append(epoch_loss)
    train_accuracies.append(epoch_acc)
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.2f}%')

model_save_path = "D:/Magisterka/Praca_magisterska/Algorytmy/Transfer_learining/resnet18_spoczynek_vs_zadanie.pth"
torch.save(model.state_dict(), model_save_path)

print("Model został zapisany.")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Funkcja straty')
plt.title('Strata podczas treningu')
plt.xlabel('Epoka')
plt.ylabel('Strata')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(train_accuracies, label='Dokładność', color='orange')
plt.title('Dokładność podczas treningu')
plt.xlabel('Epoka')
plt.ylabel('Dokładność [%]')
plt.legend()

plt.show()
