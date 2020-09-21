import nltk
import yaml
import string
import json
import os
import sys
import ast
from urllib.parse import quote
import math
from pytorch_pretrained_bert import OpenAIGPTTokenizer, OpenAIGPTModel, OpenAIGPTLMHeadModel
import ast
import torch
import nltk

sys.path.append(os.getcwd()+'/comet-commonsense')

def getParams():
	model = OpenAIGPTLMHeadModel.from_pretrained('openai-gpt')
	model.eval()
	tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
	return model,tokenizer

def getscore(sentence,tokenizer,model):
	tokenize_input = tokenizer.tokenize(sentence)
	tensor_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)])
	loss=model(tensor_input, lm_labels=tensor_input)
	return loss

def getCommonSense(utterance):
	os.system('python comet-commonsense/scripts/generate/generate_conceptnet_arbitrary.py --model_file comet-commonsense/pretrained_models/conceptnet_pretrained_model.pickle --input "'+utterance+'" --output_file output.json --device 0 --sampling_algorithm beam-5')
	output = json.load(open('output.json', "r"))
	return output[0]['HasProperty']['beams']

def create_literal(simile):
	model,tokenizer = getParams()
	vehicle = simile.split(' like a ')[1]
	tenor_event_comp = simile.split(' like a ')[0]+' like a'
	vehicle_property = getCommonSense(vehicle)
	scores = []
	for elem in vehicle_property:
		if elem not in vehicle:
			scores.append((getscore(tenor_event_comp+' '+elem,tokenizer,model),tenor_event_comp+' '+elem))
	scores.sort(key = lambda x: x[0],reverse=True)
	best_literal = scores[0][1]
	return best_literal
		

print(create_literal('Rare and forgotten words are like a strong spice'))


