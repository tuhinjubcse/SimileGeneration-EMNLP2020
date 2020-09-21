import torch
from fairseq.models.bart import BARTModel
import os
import time
import numpy as np
os.environ['CUDA_VISIBLE_DEVICES']="1"

bart = BARTModel.from_pretrained('checkpoint-similenew/',checkpoint_file='checkpoint_best.pt',data_name_or_path='similenew')

bart.cuda()
bart.eval()

np.random.seed(4)
torch.manual_seed(4)

count = 1
bsz = 1
t = 0.7
for val in [5]:
    with open('literal.txt') as source, open('simile.hypo', 'w') as fout:
        sline = source.readline().strip()
        slines = [sline]
        for sline in source:
            if count % bsz == 0:
                with torch.no_grad():
                    hypotheses_batch = bart.sample(slines, sampling=True, sampling_topk=val  ,temperature=t ,lenpen=2.0, max_len_b=30, min_len=7, no_repeat_ngram_size=3)
                for hypothesis in hypotheses_batch:
                    fout.write(hypothesis.replace('\n','') + '\n')
                    fout.flush()
                slines = []

            slines.append(sline.strip())
            count += 1
        if slines != []:
            hypotheses_batch = bart.sample(slines, sampling=True,   sampling_topk=val  ,temperature=t ,lenpen=2.0, max_len_b=30, min_len=7, no_repeat_ngram_size=3)
            for hypothesis in hypotheses_batch:
                fout.write(hypothesis.replace('\n','') + '\n')
                fout.flush()
