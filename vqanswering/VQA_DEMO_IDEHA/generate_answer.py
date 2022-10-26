#from bert import get_pretrained_bert
import pickle
#import json
import os
#from simpletransformers.question_answering import QuestionAnsweringModel
#from vqa_bottom_up_evaluation.VQA_bottom_up import data_loader,base_model
#import torch.nn as nn
#from VQA_DEMO_IDEHA.vqa_bottom_up_evaluation.VQA_bottom_up.preprocessing import _tokenize
import numpy as np
import torch.nn.functional as F
import torch
#from VQA_DEMO_IDEHA.bert_evaluation.bert_eval import normalize_answer

os.environ['CUDA_VISIBLE_DEVICES']  = ''
# test = json.load(open(os.path.join('/delorean/pietrobongini', 'artpedia.json'), 'rb'))
# test_qa = json.load(open('./vqa_bottom_up_evaluation/VQA_bottom_up/data/artpedia_vqa.json','rb'))
#
idx2word, word2idx = pickle.load(open(os.path.join('./vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_q.pkl'), 'rb'))
idx2ans, ans2idx = pickle.load(open(os.path.join('./vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_ans.pkl'), 'rb'))
# data_path = '/delorean/pietrobongini/'
# artpedia_image_folder = 'artpedia_images/'
# question_classifier = get_pretrained_bert(use_cuda=False)
# question_answering_model = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad', args={'reprocess_input_data': True, 'overwrite_output_dir': True},use_cuda=False)
# artpedia = json.load(open(data_path + 'artpedia.json', 'rb'))
# mode = 'eval'
# glove_embed_dir = './vqa_bottom_up_evaluation/VQA_bottom_up/data/glove_pretrained_300.npy'
# model_name = 'model_bs_256_adamax_grid_feats'#'bottom_up_new_att_batch_512_adamax'
# resume = './vqa_bottom_up_evaluation/VQA_bottom_up/checkpoint/' + model_name + '/best.pth.tar'
# optimizer = 'Adamax'
device = torch.device('cpu')
# num_hid = 1024
# lr = 0.002
# constructor = 'bottom_up_newatt'
# vocab_size, num_classes = len(idx2word), 3129
# model = getattr(base_model, constructor)(vocab_size, num_classes, glove_embed_dir, num_hid)
# model = nn.DataParallel(model).to(device)
#
# if optimizer == 'Adamax':
#     optim = torch.optim.Adamax(model.parameters(), lr=lr)
#
# if os.path.exists(resume):
#     print("Initialized VQA model from ckpt: " + resume)
#     ckpt = torch.load(resume, map_location=device)
#     start_epoch = ckpt['epoch']
#     model.load_state_dict(ckpt['state_dict'])
#     optim.load_state_dict(ckpt['optim_state_dict'])
#
# model.eval()


#function to load visual features
def get_img_feats(img_path):
    f = torch.load(img_path).to(device)
    return f

#TODO: before giving the context in input to ProduceAnswer remember to add to the context the sentence "this painting was depicted in 'year' "

def produceAnswer(question_classifier, model, question_answering_model, question, context, vfeats):
    predictions, raw_outputs = question_classifier.predict([question])
    if predictions[0] == 0:
        to_predict = []
        to_predict.append({'context': context, 'qas': [{'question': question, 'id': 0}]})
        a_pred = question_answering_model.predict(to_predict)[0]['answer']
        a_pred = normalize_answer(a_pred)
    else:
        seqlen = 14
        question_toked = _tokenize(question)
        que = np.ones(seqlen, dtype=np.int64) * len(word2idx)
        if len(question_toked) < seqlen:
            for i, word in enumerate(question_toked):
                if word in word2idx:
                    que[i] = word2idx[word]

        v = F.pad(vfeats ,(0,32-vfeats.size(3),0,32-vfeats.size(2)))

        q = torch.tensor(que).to(device).unsqueeze(0)
        v = v.transpose(1,3)
        logits = model(q, torch.reshape(v, (v.size(0), v.size(1)*v.size(2), v.size(3))))
        pred_cpu_idx = torch.max(logits, 1)[1].cpu()
        a_pred = idx2ans[pred_cpu_idx]
    return a_pred

def main():
    img_path = '/delorean/pietrobongini/feats_vqa_demo/artpedia/image_5299.pth'
    vfeat = get_img_feats(img_path)
    while True:
        question = input('scrivere domanda:')
        context = input('scrivere contesto')
        ans = produceAnswer(question, context, vfeat)
        print(ans)

#if __name__ == '__main__':
#    main()