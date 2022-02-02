# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 19:44:17 2021

@author: gontier
"""

# Relevant packages ##########################################################

from __future__ import print_function
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
import os
from torchvision import models
torch.cuda.empty_cache()
import numpy as np
import random

# Parameters ##################################################################

batch_size      = 20
nb_epoch        = 300
size            = 256
weight_decay    = 0.0025

torch.manual_seed(1234)
np.random.seed(31)
random.seed(32) 
torch.cuda.manual_seed_all(33)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Sets device #################################################################

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Train and test data directory ###############################################

data_dir_train = os.getcwd() + "/DELAUNAY_train"
data_dir_test = os.getcwd() + "/DELAUNAY_test"

# Loads the train and test data ###############################################

dataset_base = ImageFolder(data_dir_train,transform = transforms.Compose([
    transforms.Resize((size,size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5853, 0.5335, 0.4950],
                                             std=[0.2348, 0.2260, 0.2242]),
]))
train_dataset, val_dataset = torch.utils.data.random_split(dataset_base, 
                                                           [7362, 1840],
    generator=torch.Generator().manual_seed(42))

test_dataset = ImageFolder(data_dir_test,transform = transforms.Compose([
    transforms.Resize((size,size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5853, 0.5335, 0.4950],
                                             std=[0.2348, 0.2260, 0.2242]),
]))

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, 
    pin_memory=True,
    generator=torch.Generator().manual_seed(43)
)

val_loader = torch.utils.data.DataLoader(
    val_dataset, batch_size=batch_size, shuffle=True, num_workers=4, 
    pin_memory=True,
    generator=torch.Generator().manual_seed(44)
)

test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=batch_size, shuffle=True, num_workers=4, 
    pin_memory=True,
    generator=torch.Generator().manual_seed(45)
)

# Classes ####################################################################

classes = ('Ad Reinhardt', 'Alberto Magnelli', 'Alfred Manessier', 'Anthony Caro', 
            'Antoine Pevsner', 'Auguste Herbin', 'Aurélie Nemours', 'Berto Lardera', 
            'Charles Lapicque', 'Charmion Von Wiegand', 'César Domela', 'Ellsworth Kelly', 
            'Emilio Vedova', 'Fernand Léger', 'František Kupka', 'Franz Kline', 
            'François Morellet', 'Georges Mathieu', 'Georges Vantongerloo', 
            'Gustave Singier', 'Hans Hartung', 'Jean Arp', 'Jean Bazaine', 'Jean Degottex', 
            'Jean Dubuffet', 'Jean Fautrier', 'Jean Gorin', 'Joan Mitchell', 
            'Josef Albers', 'Kenneth Noland', 'Leon Polk Smith', 'Lucio Fontana', 
            'László Moholy-Nagy', 'Léon Gischia', 'Maria Helena Vieira da Silva', 
            'Mark Rothko', 'Morris Louis', 'Naum Gabo', 'Olle Bærtling', 'Otto Freundlich', 
            'Pierre Soulages', 'Pierre Tal Coat', 'Piet Mondrian', 'Richard Paul Lohse', 
            'Roger Bissière', 'Sam Francis', 'Sonia and Robert Delaunay', 'Sophie Taeuber-Arp', 
            'Theo van Doesburg', 'Vassily Kandinsky', 'Victor Vasarely', 'Yves Klein', 'Étienne Béothy')

# CNN ########################################################################

net = models.resnet152(pretrained=False)
net.to(device)

# Loss function and optimizer ################################################

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.003, weight_decay=weight_decay)

# Training ###################################################################

train_error_values = []
val_error_values = []

for epoch in range(nb_epoch):

    # Train ##################################################################
    running_loss = 0.0
    
    for i, data in enumerate(train_loader, 0):
        
        inputs, labels = data[0].to(device), data[1].to(device)

        optimizer.zero_grad()

        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    running_loss = running_loss / len(train_loader)
    
    # display the epoch training loss
    print("epoch : {}/{}, loss_recons = {:.6f}".format(epoch + 1, nb_epoch, running_loss))
    
    # Compute training error #################################################
    
    correct = 0
    total = 0

    with torch.no_grad():
        for data in train_loader:
            images, labels = data[0].to(device), data[1].to(device)

            outputs = net(images)

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    print('Accuracy of the network on the training images: %d %%' % (
        100 * correct / total))
    train_error_values.append(100 - 100 * correct / total)
    
    ###################################################################
    
    # Val ###################################################################
    correct = 0
    total = 0

    with torch.no_grad():
        for data in val_loader:
            images, labels = data[0].to(device), data[1].to(device)

            outputs = net(images)

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    print('Accuracy of the network on the validation images: %d %%' % (
        100 * correct / total))
    val_error_values.append(100 - 100 * correct / total)
        
# Test ###################################################################

correct = 0
total = 0

with torch.no_grad():
    for data in test_loader:
        images, labels = data[0].to(device), data[1].to(device)

        outputs = net(images)

        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print('Accuracy of the network on the test images: %d %%' % (
    100 * correct / total))
test_error_values=(100 - 100 * correct / total)

print('Finished Training')

# Final results ##############################################################

correct_pred = {classname: 0 for classname in classes}
total_pred = {classname: 0 for classname in classes}

with torch.no_grad():
    for data in test_loader:
        images, labels = data
        images, labels = images.to(device), labels.to(device)
        outputs = net(images)
        _, predictions = torch.max(outputs, 1)

        for label, prediction in zip(labels, predictions):
            if label == prediction:
                correct_pred[classes[label]] += 1
            total_pred[classes[label]] += 1

accuracy_values = []

for classname, correct_count in correct_pred.items():
    accuracy = 100 * float(correct_count) / total_pred[classname]
    print("Accuracy for class {:5s} is: {:.1f} %".format(classname,
                                                   accuracy))
    accuracy_values.append(accuracy)
    
# Confusion matrix ##############################################################

y_pred = []
y_true = []

for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        output = net(inputs) 

        output = (torch.max(torch.exp(output), 1)[1]).data.cpu().numpy()
        y_pred.extend(output) 
        
        labels = labels.data.cpu().numpy()
        y_true.extend(labels) 
