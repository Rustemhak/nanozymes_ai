import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

import pandas as pd

from src.logger import Logger

def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-large')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
Logger.info(f"Downloaded model: {model}, device: {device}")
def e5_get_embeddings(knowledge_texts):
    # каждый элемент обязательно начинается с "passage:"
    passage_batch_dict = tokenizer(knowledge_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')
    passage_outputs = model(**passage_batch_dict.to(device))
    passage_embeddings = average_pool(passage_outputs.last_hidden_state, passage_batch_dict['attention_mask'])
    passage_embeddings = F.normalize(passage_embeddings, p=2, dim=1)
    return passage_embeddings
