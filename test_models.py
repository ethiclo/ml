"""
Module for testing the model
"""

from models.classification.classification_classes import ResNet15, classify_img, classes
import torch

# Load the model
model = ResNet15(3, len(classes))
model.load_state_dict(torch.load('models/classification/clothing_model_weights.pt'))

src = 'https://cdn.shopify.com/s/files/1/1084/7742/products/58_3f7c2d27-e84f-4d07-82f1-a45554150376_800x.jpg?v=1667801579'
classify_img(src, model)

