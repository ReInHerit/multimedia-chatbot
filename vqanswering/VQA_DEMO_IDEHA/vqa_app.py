from flask import Flask
from flask import render_template, request, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from wtforms import Form, StringField, validators
from VQA_DEMO_IDEHA.generate_answer import produceAnswer
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
import sys
from transformers import BertTokenizer, BertForQuestionAnswering

os.environ['CUDA_VISIBLE_DEVICES'] = ''

idx2word, word2idx = pickle.load(
    open(os.path.join('./vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_q.pkl'), 'rb'))
idx2ans, ans2idx = pickle.load(
    open(os.path.join('./vqa_bottom_up_evaluation/VQA_bottom_up/data', 'dict_ans.pkl'), 'rb'))
data_path = '/delorean/pietrobongini/'
question_classifier = get_pretrained_bert(use_cuda=False)
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
qamodel = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# question_answering_model = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad', args={'reprocess_input_data': True, 'overwrite_output_dir': True},use_cuda=False)
mode = 'eval'
glove_embed_dir = './vqa_bottom_up_evaluation/VQA_bottom_up/data/glove_pretrained_300.npy'
model_name = 'model_bs_256_adamax_grid_feats'  # 'bottom_up_new_att_batch_512_adamax'
resume = './vqa_bottom_up_evaluation/VQA_bottom_up/checkpoint/' + model_name + '/best.pth.tar'
optimizer = 'Adamax'
device = torch.device('cpu')
num_hid = 1024
lr = 0.002
constructor = 'bottom_up_newatt'
vocab_size, num_classes = len(idx2word), 3129
model = getattr(base_model, constructor)(vocab_size, num_classes, glove_embed_dir, num_hid)
model = nn.DataParallel(model).to(device)

if optimizer == 'Adamax':
    optim = torch.optim.Adamax(model.parameters(), lr=lr)

if os.path.exists(resume):
    print("Initialized VQA model from ckpt: " + resume)
    ckpt = torch.load(resume, map_location=device)
    start_epoch = ckpt['epoch']
    model.load_state_dict(ckpt['state_dict'])
    optim.load_state_dict(ckpt['optim_state_dict'])

model.eval()


class VQAForm(FlaskForm):
    question = StringField('question:', validators=[validators.required()])
    context = StringField('context:', validators=[validators.required()])
    image = StringField('image:', validators=[validators.required()])  # validators=[FileRequired('File was empty!')])
    submit = SubmitField('Upload')


feats_extractor = load_model(None)

app = Flask(__name__)
PAINTINGS_FOLDER = os.path.join('static', 'paintings')
app.config['UPLOAD_FOLDER'] = PAINTINGS_FOLDER
CSS_FOLDER = os.path.join('static', 'style')
app.config['CSS_FOLDER'] = CSS_FOLDER
app.config['SECRET_KEY'] = 'asjhcsfpic'


@app.route("/", methods=['GET', 'POST'], )
def display_home():
    answer = ""
    form = VQAForm()
    css_dir = os.path.join(app.config['CSS_FOLDER'], 'style.css')
    if request.method == 'POST':
        if form.validate_on_submit():

            # image = Image.open(request.form['image']) #Image.open(io.BytesIO(form.image.data.stream.read()))
            question = request.form['question']

            feat_path = './VQA_DEMO_IDEHA/image_features/' + request.form['image'].split('/')[-1].split('.')[0] + '.pth'
            if os.path.isfile(feat_path):
                print('loading feats...')
                vfeats = torch.load(feat_path)
            else:
                print('computing feats...')
                image = Image.open(request.form['image'])
                vfeats = gen_feats(feats_extractor, image)
                torch.save(vfeats, feat_path)
            context = request.form['context']
            answer = produceAnswer(question_classifier, model, qamodel, tokenizer, question, context, vfeats)

            return jsonify({'answer': answer})
        # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], request.form['image'])

        return render_template('vqa_form.html', form=form, css_path=css_dir, answer=answer)

    if request.method == 'GET':
        return render_template('vqa_form.html', form=form, css_path=css_dir, answer=answer)


# if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=80)
from glob import glob
from os import getcwd, chdir
from tqdm import tqdm
import numpy as np

path = '/oblivion/users/pietrobongini/VisualDialog/VisualDialog_test2018/'
feat_path = '/oblivion/users/pietrobongini/VisualDialog/VisualDialog_test2018_feats/'
if os.path.isdir(feat_path) == False:
    os.mkdir(feat_path)
chdir(path)
print('starting...')
for f in tqdm(glob('*.jpg')):
    f_name = f.split('_')[-1].split('.')[0].lstrip('0') + '.pth'
    image = Image.open(path + f)
    vfeats = gen_feats(feats_extractor, image)
    torch.save(vfeats, feat_path + f_name)
print('end.')
