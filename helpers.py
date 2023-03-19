import torch

# Get the classification model
from models.classification.classification_classes import ResNet15, classify_img, classes

# Get the scraper
from scraper import scrape_website_text, get_imgs, sustainability_search

def handle_url(url):

    # Get the sustainability words and image from the URL
    web_text = scrape_website_text(url)
    imgs = get_imgs(url)
    alt_text = imgs[0]
    image = imgs[1]

    # Load the classification model
    model = ResNet15(3, len(classes))
    model.load_state_dict(torch.load('models/classification/clothing_model_weights.pt'))
    
    # Classify the image
    classification = classify_img(image, model)

    # Give it a score
    # TODO: Add scoring model once completed
    score = 0

    # Return the data
    return {
        'url': url,
        'image': image,
        'title': alt_text,
        'price': web_text['price'],
        'brand': web_text['brand'],
        'description': 'description',
        'score': score,
        'classification': classification,
    }

def predict_sustainability():
    """Predict the sustainability of a product."""