from transformers import BartTokenizer, BartForConditionalGeneration
from datasets import load_dataset

# Data loading
dataset = load_dataset('xsum', save_infos=True)

# Data Preprocessing
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
# ['train'] 데이터에서 document->input_ids, summary->decoder_input_ids, tokenizer 사용
for data in dataset['train']:
    data['document']
# 변환 후 csv 파일 변환 저장

model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")
# model forward()
# input_ids: 모델의 input
# attention_mask: 시퀀스 길이를 동일하게 만들기 위한 masking
# decoder_input_ids: 모델 디코더 input(번역 혹은 요약 training 에서, 필수적임), 없을 경우 input_ids 그대로 입력함.
