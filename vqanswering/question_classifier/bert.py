import pandas as pd
import numpy as np
from simpletransformers.classification import ClassificationModel


def generate_bert_dataset(dataset, split):
    text = []
    label = []
    for num, ex in enumerate(dataset):
        text.append(ex['question'][0].lower().replace(',', '').replace('?', ''))
        label.append(np.argmax(ex['question_type']))
    d = {
        'text': text,
        'alpha': label,
    }
    df = pd.DataFrame(data=d).sample(frac=1)
    return df


def get_pretrained_bert(use_cuda=True):
    print('importing question_classifier...')
    # Create a ClassificationModel
    model = ClassificationModel('bert', './question_classifier/models/vqa_bert', use_cuda=use_cuda) # 'bert-base-cased')
    return model
