from datasets import load_dataset
from transformers import BartTokenizer
import pandas as pd
import re

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")


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
pd_data = {'document': [], 'summary': []}
pd_data = pd.DataFrame(data=pd_data)

count = 0
for data in dataset['train']:
    x_data, y_data = preprocessing_data(data)
    data_to_insert = {'document': x_data, 'summary': y_data}
    pd_data.append(data_to_insert)
    count += 1
    if count % 10000 == 0:
        print(count)

pd_data.to_csv('storage/dataset_preprocessing.csv', index=True)
