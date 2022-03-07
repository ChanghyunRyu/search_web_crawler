from datasets import load_dataset
from transformers import BartTokenizer, BartForConditionalGeneration
import re
import torch

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")


def preprocessing_data(data):
    x_data = data['document']
    x_data = re.sub('\n', '', x_data)
    y_data = data['summary']

    x_data = tokenizer(x_data, truncation=True, max_length=1024, return_tensors='pt')
    y_data = tokenizer(y_data, truncation=True, max_length=512, return_tensors='pt')

    return x_data, y_data


# Dataset load
dataset = load_dataset('xsum', save_infos=True)
input_data = []
decode_data = []

model.train()
count = 0
for data in dataset['train']:
    x_data, y_data = preprocessing_data(data)
    model.forward(input_ids=x_data['input_ids'], attention_mask=x_data['attention_mask'],
                  decoder_input_ids=y_data['input_ids'], decoder_attention_mask=y_data['attention_mask'])
    count += 1
    print(count)
    if count % 10000:
        print(count)
        torch.save(model.state_dict(), "model/epoch_{0:d}.pt".format('10000'))


