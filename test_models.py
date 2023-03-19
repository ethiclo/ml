"""
Module for testing the model
"""

from models.classification.classification_classes import ResNet15, classify_img, classes
from models.scoring.scoring_classes import predict_sustainability
import torch

# First, we classify the image
#Load the model
model = ResNet15(3, len(classes))
model.load_state_dict(torch.load('models/classification/clothing_model_weights.pt'))

src = 'https://cdn.shopify.com/s/files/1/1084/7742/products/58_3f7c2d27-e84f-4d07-82f1-a45554150376_800x.jpg?v=1667801579'
print(classify_img(src, model))

# Then we score it on its sustainability based on the brand
# Example input texts (replace these with your own texts)
texts = ["adidas reebok", "calvin klein organic cotton", "nike fairtrade"]

# Make predictions
predictions = predict_sustainability(texts)
print(predictions.tolist())

# Print predictions
for text, prediction in zip(texts, predictions):
    print(f"Text: {text}, Score: {prediction:.4f}")

