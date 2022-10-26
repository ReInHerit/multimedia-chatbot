import torch
from transformers import *

# Transformers has a unified API
# for 8 transformer architectures and 30 pretrained weights.
#          Model          | Tokenizer          | Pretrained weights shortcut
MODELS = [(BertModel, BertTokenizer, 'bert-base-uncased'),
          (OpenAIGPTModel, OpenAIGPTTokenizer, 'openai-gpt'),
          (GPT2Model, GPT2Tokenizer, 'gpt2'),
          (CTRLModel, CTRLTokenizer, 'ctrl'),
          (TransfoXLModel, TransfoXLTokenizer, 'transfo-xl-wt103'),
          (XLNetModel, XLNetTokenizer, 'xlnet-base-cased'),
          (XLMModel, XLMTokenizer, 'xlm-mlm-enfr-1024'),
          (DistilBertModel, DistilBertTokenizer, 'distilbert-base-uncased'),
          (RobertaModel, RobertaTokenizer, 'roberta-base')]

# To use TensorFlow 2.0 versions of the models, simply prefix the class names with 'TF', e.g. `TFRobertaModel` is the TF 2.0 counterpart of the PyTorch model `RobertaModel`

# Let's encode some text in a sequence of hidden-states using each model:
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
question, text = "how are the farmers seated?", 'Abraham Lincoln is an 1869 oil-on-canvas painting by George Peter Alexander Healy of Abraham Lincoln the 16th President of the United States The pose is taken from Healys 1868 painting The Peacemakers which depicts the historic March 28 1865 strategy session by the Union high command composed of William Tecumseh Sherman Ulysses S Grant David Dixon Porter and Lincoln aboard the steamboat the River Queen during the final days of the American Civil War the title of this painting is Abraham Lincoln (Healy) this painting was depicted in 1869'
input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
input_ids = tokenizer.encode(input_text)
token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))]
start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
print(all_tokens)
print(' '.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1]))
# a nice puppet
