from transformers import BertTokenizer, BertModel
import torch.nn as nn
import torch

class BERTRegressor(nn.Module):
    def __init__(self):
        super(BERTRegressor, self).__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.fc = nn.Linear(self.bert.config.hidden_size, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        cls_token = last_hidden_state[:, 0, :]
        score = self.fc(cls_token)
        return score.squeeze()
    
def load_model():
    model = BERTRegressor()
    model.load_state_dict(torch.load("models/scoring/prediction_model_weights.pt"))

    # Load the tokenizer's configuration and vocabulary
    tokenizer = BertTokenizer.from_pretrained("models/scoring/tokenizer")
    return model, tokenizer

def predict_sustainability(texts, max_length=128, device="cpu"):
    model, tokenizer = load_model()
    model.eval()
    model.to(device)

    # Tokenize the input texts
    encoded_texts = tokenizer.batch_encode_plus(
        texts,
        add_special_tokens=True,
        max_length=max_length,
        return_token_type_ids=False,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors="pt",
    )

    input_ids = encoded_texts["input_ids"].to(device)
    attention_mask = encoded_texts["attention_mask"].to(device)

    # Make predictions
    with torch.no_grad():
        predictions = model(input_ids, attention_mask)
    
    return predictions.cpu().numpy()