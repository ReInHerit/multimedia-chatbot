from VQA_DEMO_IDEHA.grid_feats_vqa_master.extract_grid_feature import gen_feats, load_model
import os
from VQA_DEMO_IDEHA.bert import get_pretrained_bert
import pickle
import os
from simpletransformers.question_answering import QuestionAnsweringModel
from VQA_DEMO_IDEHA.vqa_bottom_up_evaluation.VQA_bottom_up import base_model
import torch.nn as nn
from PIL import Image
import torch
import requests
import shutil
from VQA_DEMO_IDEHA.vqa_bottom_up_evaluation.VQA_bottom_up.preprocessing import _tokenize
from VQA_DEMO_IDEHA.bert_evaluation.bert_eval import normalize_answer
import numpy as np
import torch.nn.functional as F

os.environ['CUDA_VISIBLE_DEVICES'] = ''

device = torch.device('cpu')


# def extract_models_for_answer():
def download_image(image_url):
    r = requests.get(image_url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        # with open(filename, 'wb') as f:
        # shutil.copyfileobj(r.raw, f)
        img = Image.open(r.raw)
        return img
    else:
        return 0


class AnswerGenerator():
    def __init__(self):
        super(AnswerGenerator, self).__init__()
        self.idx2word, self.word2idx = pickle.load(
            open(os.path.join('../VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_q.pkl'), 'rb'))
        self.idx2ans, self.ans2idx = pickle.load(
            open(os.path.join('./VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_ans.pkl'), 'rb'))
        data_path = '/delorean/pietrobongini/'
        self.question_classifier = get_pretrained_bert(use_cuda=False)
        self.question_answering_model = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad',
                                                               args={'reprocess_input_data': True,
                                                                     'overwrite_output_dir': True}, use_cuda=False)
        mode = 'eval'
        glove_embed_dir = './VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/data/glove_pretrained_300.npy'
        model_name = './VQA_DEMO_IDEHA/model_bs_256_adamax_grid_feats'  # 'bottom_up_new_att_batch_512_adamax'
        resume = './VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/checkpoint/' + model_name + '/best.pth.tar'
        optimizer = 'Adamax'
        device = torch.device('cpu')
        num_hid = 1024
        lr = 0.002
        constructor = 'bottom_up_newatt'
        vocab_size, num_classes = len(self.idx2word), 3129
        model = getattr(base_model, constructor)(vocab_size, num_classes, glove_embed_dir, num_hid)
        self.model = nn.DataParallel(model).to(device)
        self.feats_extractor = load_model(None)
        if optimizer == 'Adamax':
            optim = torch.optim.Adamax(model.parameters(), lr=lr)

        if os.path.exists(resume):
            print("Initialized VQA model from ckpt: " + resume)
            ckpt = torch.load(resume, map_location=device)
            start_epoch = ckpt['epoch']
            self.model.load_state_dict(ckpt['state_dict'])
            optim.load_state_dict(ckpt['optim_state_dict'])

        model.eval()

    def get_models(self):
        return self.model, self.question_classifier, self.question_answering_model

    def get_image_features(self, url_path):
        feat_path = './image_features/' + url_path.split('/')[-1].split('.')[0] + '.pth'
        if os.path.isfile(feat_path):
            print('loading feats...')
            vfeats = torch.load(feat_path)
        else:
            print('computing feats...')
            image = download_image(url_path)  # Image.open(request.form['image'])
            vfeats = gen_feats(self.feats_extractor, image)
            torch.save(vfeats, feat_path)
        return vfeats

    def produceAnswer(self, question, context, vfeats):
        predictions, raw_outputs = self.question_classifier.predict([question])
        if predictions[0] == 0:
            to_predict = []
            to_predict.append({'context': context, 'qas': [{'question': question, 'id': 0}]})
            a_pred = self.question_answering_model.predict(to_predict)[0]['answer']
            a_pred = normalize_answer(a_pred)
        else:
            seqlen = 14
            question_toked = _tokenize(question)
            que = np.ones(seqlen, dtype=np.int64) * len(self.word2idx)
            if len(question_toked) < seqlen:
                for i, word in enumerate(question_toked):
                    if word in self.word2idx:
                        que[i] = self.word2idx[word]

            v = F.pad(vfeats, (0, 32 - vfeats.size(3), 0, 32 - vfeats.size(2)))

            q = torch.tensor(que).to(device).unsqueeze(0)
            v = v.transpose(1, 3)
            logits = self.model(q, torch.reshape(v, (v.size(0), v.size(1) * v.size(2), v.size(3))))
            pred_cpu_idx = torch.max(logits, 1)[1].cpu()
            a_pred = self.idx2ans[pred_cpu_idx]
        return a_pred
