import pickle
import pandas as pd
import numpy as np
import os
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


def get_pretrained_bert(use_cuda = True):
    #train = pickle.load(open(os.path.join('data', 'train_qa_ovqa.pkl'), 'rb'))
    #test = pickle.load(open(os.path.join('data', 'val_qa_ovqa.pkl'), 'rb'))
    #train_df = generate_bert_dataset(train, split='train')
    #eval_df = generate_bert_dataset(test, split='dev')
    # Train and Evaluation data needs to be in a Pandas Dataframe of two columns. The first column is the text with type str, and the second column is the label with type int.
    #train_data = [['Example sentence belonging to class 1', 1], ['Example sentence belonging to class 0', 0]]
    #train_df = pd.DataFrame(train_data)

    #eval_data = [['Example eval sentence belonging to class 1', 1], ['Example eval sentence belonging to class 0', 0]]
    #eval_df = pd.DataFrame(eval_data)
    print('importing question_classifier...')
    # Create a ClassificationModel
    model = ClassificationModel('bert', 'C:\\Users\\arkfil\Desktop\demo_icpr\\vqanswering\VQA_DEMO_IDEHA\outputs\\vqa_bert', use_cuda=use_cuda)#'bert-base-cased')
    return model
    # Train the model
    #model.train_model(train_df)
    #result, model_outputs, wrong_predictions = model.eval_model(eval_df)
