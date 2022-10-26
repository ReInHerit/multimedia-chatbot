from bert import get_pretrained_bert
import pickle
import json
import os
from simpletransformers.question_answering import QuestionAnsweringModel
from bert_evaluation.bert_eval import normalize_answer, compute_exact, compute_f1, make_eval_dict, get_raw_scores, \
    apply_no_ans_threshold, merge_eval, find_best_thresh
from transformers import *
import torch
from bert import get_pretrained_bert

test = json.load(open(os.path.join('/delorean/pietrobongini', 'artpedia.json'), 'rb'))
test_qa = json.load(open('../annotator_VQA/artpedia_vqa/artpedia_vqa.json', 'rb'))
# ex = test['11085']
# os.system("/equilibrium/pietrobongini/bottom-up-attention-master/tools/demo.py")


# activate_this = "/equilibrium/pietrobongini/bottom-up-attention-master/caffe/venvvqa/bin/activate_this.py"
# exec(open(activate_this).read())#, dict(__file__=activate_this))

# for sent in ex['contextual_sentences']:
#     contextual_sentence += sent + ' '    #sent.replace(',', '').replace('.', '')
# print(contextual_sentence)

question_classifier = get_pretrained_bert()
question_answering_model = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad',
                                                  args={'reprocess_input_data': True, 'overwrite_output_dir': True})

# while True:
exact_scores = {}
f1_scores = {}
qid_to_has_ans = {}
preds = {}
qid = 0
count_contextual = 0
count_visual = 0
for key in test_qa.keys():
    ex = test[key]
    contextual_sentence = ''
    for sent in ex['contextual_sentences']:
        contextual_sentence += sent + ' '  # sent.replace(',', '').replace('.', '')
    sent = 'this painting was depicted in ' + str(test[key]['year'])
    contextual_sentence += sent
    print(contextual_sentence)

    for question, answer in test_qa[key]['contextual_qa']:
        to_predict = []
        to_predict.append({'context': contextual_sentence, 'qas': [{'question': question, 'id': 0}]})
        a_pred = question_answering_model.predict(to_predict)[0]['answer']
        print('q: ', question, 'a: ', answer, 'pred:', a_pred)

        gold_answers = [normalize_answer(answer)]
        # Take max over all gold answers
        exact_scores[qid] = max(compute_exact(a, a_pred) for a in gold_answers)
        f1_scores[qid] = max(compute_f1(a, a_pred) for a in gold_answers)
        qid_to_has_ans[qid] = 1
        preds[qid] = a_pred
        qid += 1
        predictions, raw_outputs = question_classifier.predict([question])
        if predictions[0] == 0:
            count_contextual += 1
        print('pred num contextual: ', count_contextual)

# for key in test_qa.keys():
#     ex = test[key]
#     visual_sentence = ''
#     for sent in ex['visual_sentences']:
#         visual_sentence += sent + ' '  # sent.replace(',', '').replace('.', '')
#     sent = 'this painting was depicted in '+str(test[key]['year'])
#     visual_sentence += sent
#     print(visual_sentence)
#
#     for question, answer in test_qa[key]['visual_qa']:
#     #question = input('question: ')
#     #predictions, raw_outputs = question_classifier.predict([question])
#     #if predictions[0] == 0:
#
#         to_predict = []
#         to_predict.append({'context': visual_sentence, 'qas':[{'question': question, 'id': 0}]})
#         a_pred =question_answering_model.predict(to_predict)[0]['answer']
#         print('q: ', question, 'a: ',answer, 'pred:', a_pred)
#
#         gold_answers = [normalize_answer(answer)]
#         # Take max over all gold answers
#         exact_scores[qid] = max(compute_exact(a, a_pred) for a in gold_answers)
#         f1_scores[qid] = max(compute_f1(a, a_pred) for a in gold_answers)
#         qid_to_has_ans[qid] = 1
#         preds[qid] = a_pred
#         qid += 1


na_probs = {k: 0.0 for k in range(0, qid)}
print(make_eval_dict(exact_scores, f1_scores))
has_ans_qids = [k for k, v in qid_to_has_ans.items() if v]
no_ans_qids = [k for k, v in qid_to_has_ans.items() if not v]
exact_raw = exact_scores
f1_raw = f1_scores

_, tresh = find_best_thresh(preds, exact_raw, na_probs, qid_to_has_ans)
print(tresh)
exact_thresh = apply_no_ans_threshold(exact_raw, na_probs, qid_to_has_ans, 0)
# OPTS.na_prob_thresh)
f1_thresh = apply_no_ans_threshold(f1_raw, na_probs, qid_to_has_ans, 0)
# OPTS.na_prob_thresh)
out_eval = make_eval_dict(exact_thresh, f1_thresh)

if has_ans_qids:
    has_ans_eval = make_eval_dict(exact_thresh, f1_thresh, qid_list=has_ans_qids)
    merge_eval(out_eval, has_ans_eval, 'HasAns')
if no_ans_qids:
    no_ans_eval = make_eval_dict(exact_thresh, f1_thresh, qid_list=no_ans_qids)
    merge_eval(out_eval, no_ans_eval, 'NoAns')
    # elif predictions[0] == 1:
    #    print('Visual Question')
print(out_eval)
