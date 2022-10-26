
#from VQA_DEMO_IDEHA.grid_feats_vqa_master.extract_grid_feature import gen_feats, load_model
import os
from VQA_DEMO_IDEHA.bert import get_pretrained_bert
import pickle
import os
#from simpletransformers.question_answering import QuestionAnsweringModel
#from VQA_DEMO_IDEHA.vqa_bottom_up_evaluation.VQA_bottom_up import base_model
import torch.nn as nn
from PIL import Image
import torch
import requests
import shutil
from transformers import AutoTokenizer, BertForQuestionAnswering, pipeline, DistilBertForQuestionAnswering, DistilBertTokenizer, ViltProcessor, ViltForQuestionAnswering
import torch
#from VQA_DEMO_IDEHA.vqa_bottom_up_evaluation.VQA_bottom_up.preprocessing import _tokenize
#from VQA_DEMO_IDEHA.bert_evaluation.bert_eval import normalize_answer
import numpy as np
import torch.nn.functional as F
from collections import OrderedDict
#from googletrans import Translator
from google_trans_new import google_translator
os.environ['CUDA_VISIBLE_DEVICES']  = '0'

device = torch.device('cpu')
#def extract_models_for_answer():
def download_image(image_url):
    url = image_url
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    r = requests.get(url, headers = headers, stream=True)

    # Check if the image was retrieved successfully
    print(r.status_code)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        #with open(filename, 'wb') as f:
        #shutil.copyfileobj(r.raw, f)
        img =Image.open(r.raw)
        return img
    else:
        return 0

class AnswerGenerator():
    def __init__(self):
        super(AnswerGenerator, self).__init__()
        #self.idx2word, self.word2idx = pickle.load(open(os.path.join('./VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_q.pkl'), 'rb'))
        #self.idx2ans, self.ans2idx = pickle.load(open(os.path.join('./VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_ans.pkl'), 'rb'))
        #data_path = '/delorean/pietrobongini/'
        self.question_classifier = get_pretrained_bert(use_cuda=False)
        self.translator = google_translator()#Translator()
        device = torch.device('cpu')
        #self.question_answering_model = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad', args={'reprocess_input_data': True, 'overwrite_output_dir': True},use_cuda=False)


        modelname = 'distilbert-base-uncased' #'deepset/bert-base-cased-squad2'

        self.vqamodel = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad') #BertForQuestionAnswering.from_pretrained(modelname)
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',return_token_type_ids = True) #AutoTokenizer.from_pretrained(modelname)
        self.vqamodel.eval()
        self.vilt = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.vilt_processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.vilt.eval()
        #self.nlp = pipeline('question-answering', model=self.vqamodel, tokenizer=self.tokenizer)

        # mode = 'eval'
        # glove_embed_dir = './VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/data/glove_pretrained_300.npy'
        # model_name = 'model_bs_256_adamax_grid_feats'#'bottom_up_new_att_batch_512_adamax'
        # resume = './VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/checkpoint/' + model_name + '/best.pth.tar'
        # optimizer = 'Adamax'
        #
        # num_hid = 1024
        # lr = 0.002
        # constructor = 'bottom_up_newatt'
        # vocab_size, num_classes = len(self.idx2word), 3129
        # model = getattr(base_model, constructor)(vocab_size, num_classes, glove_embed_dir, num_hid)
        # self.vqa_model_device = 'cpu' #'cuda'
        # print(model)
        # self.model = model.to(self.vqa_model_device) #nn.DataParallel(model).to(self.vqa_model_device) # model.to(self.vqa_model_device)

        # self.feats_extractor = load_model(None)
        # if optimizer == 'Adamax':
        #     optim = torch.optim.Adamax(model.parameters(), lr=lr)

        # print('RESUMING...')
        # if os.path.exists(resume):
        #     print("Initialized VQA model from ckpt: " + resume)
        #     ckpt = torch.load(resume, map_location=self.vqa_model_device)
        #     #print('STATE DICT CKPT')
        #     #print(ckpt['state_dict'])
        #     #print('---------------------------')
        #     sd = ckpt['state_dict']
        #     new_state_dict = OrderedDict()
        #     for k, v in sd.items():
        #         name = k[7:]  # remove `module.`
        #         new_state_dict[name] = v
        #     start_epoch = ckpt['epoch']
        #     self.model.load_state_dict(new_state_dict)
        #     optim.load_state_dict(ckpt['optim_state_dict'])

            #torch.save(self.model.module.state_dict(), './VQA_DEMO_IDEHA/vqa_bottom_up_evaluation/VQA_bottom_up/checkpoint/' + model_name + '/best_simp.pth.tar')
            #print('saved')
        # self.model.eval()

    def get_models(self):
        return self.model, self.question_classifier, self.question_answering_model

    def get_image_features(self, url_path):
        feat_path = '/equilibrium/pietrobongini/demo_icpr/vqanswering/VQA_DEMO_IDEHA/image_features/' + url_path.split('/')[-1].split('.')[0]+ '.pth'
        print(feat_path)
        if os.path.isfile(feat_path):
            print('loading feats...')
            vfeats = torch.load(feat_path)
        else:
            print('computing feats...')
            print(url_path)
            image = download_image(url_path)#Image.open(request.form['image'])
            print(image)
            vfeats = gen_feats(self.feats_extractor, image)
            torch.save(vfeats, feat_path)
        return vfeats

    def produceAnswer(self, question, context, vfeats):
        #print(question)
        #tras = self.translator.translate(question, lang_src='it', lang_tgt='en')
        #question = tras #.text
        print(question)
        predictions, raw_outputs = self.question_classifier.predict([question])
        print(predictions[0])
        if predictions[0] == 0:
            self.tokenizer.encode_plus(question)

            encoding = self.tokenizer(question, context, return_tensors='pt', truncation=True, max_length=512)#r.encode_plus(question, context)

            #input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

            if len(encoding.input_ids) > 512:
                print(encoding.input_ids)
                encoding.input_ids = encoding.input_ids[:510]
                encoding.attention_mask = encoding.attention_mask[:510]
                encoding.token_type_ids = encoding.token_type_ids[:510]
            outputs = self.vqamodel(**encoding)
            answer_start_index = outputs.start_logits.argmax()
            answer_end_index = outputs.end_logits.argmax()
            predict_answer_tokens = encoding.input_ids[0, answer_start_index: answer_end_index + 1]
            answer_tokens_to_string = self.tokenizer.decode(predict_answer_tokens)
            #self.vqamodel(torch.tensor([input_ids]), attention_mask=torch.tensor([attention_mask]))

            # ans_tokens = input_ids[torch.argmax(start_scores): torch.argmax(end_scores) + 1]
            # answer_tokens = self.tokenizer.convert_ids_to_tokens(ans_tokens, skip_special_tokens=True)
            # answer_tokens_to_string = self.tokenizer.convert_tokens_to_string(answer_tokens)
            a_pred = answer_tokens_to_string

        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
            image = Image.open(requests.get(url=vfeats, headers=headers, stream=True).raw)
            print(image.size)
            if max(image.size[0], image.size[1]) > 1600:
                scale_rate = 1600 / max(image.size[0], image.size[1])
                x = int(image.size[1] * scale_rate)
                y = int(image.size[0] * scale_rate)
                image = image.resize((x,y))
            encoding = self.vilt_processor(image, question, return_tensors='pt')
            outputs = self.vilt(**encoding)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            a_pred = self.vilt.config.id2label[idx]
            # seqlen = 14
            # question_toked = _tokenize(question)
            # que = np.ones(seqlen, dtype=np.int64) * len(self.word2idx)
            # if len(question_toked) < seqlen:
            #     for i, word in enumerate(question_toked):
            #         if word in self.word2idx:
            #             que[i] = self.word2idx[word]
            #
            # v = F.pad(vfeats, (0, 32 - vfeats.size(3), 0, 32 - vfeats.size(2))).to(self.vqa_model_device)
            # q = torch.tensor(que).to(device).unsqueeze(0).to(self.vqa_model_device)
            # v = v.transpose(1, 3)
            # self.model.eval()
            # logits = self.model(q, torch.reshape(v, (v.size(0), v.size(1) * v.size(2), v.size(3))))
            # pred_cpu_idx = torch.max(logits, 1)[1].cpu()
            # a_pred = self.idx2ans[pred_cpu_idx]




        if type(a_pred) != list:
            a_pred = a_pred.split('.')[0]

        return a_pred