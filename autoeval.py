import csv
from nltk.translate.bleu_score import corpus_bleu
from bert_score import score
import os
os.environ['CUDA_VISIBLE_DEVICES']='1'

bleu1 = 0.0
bs = 0.0
r = []
c = []
with open('./human_labels.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            reference = [row[0],row[1]]
            candidate = [row[2]]
            r.append([row[0].split(),row[1].split()])
            c.append([row[2].split()])
            P_mul, R_mul, F_mul = score(candidate, reference, lang="en", rescale_with_baseline=True)
            F_mul = F_mul.tolist()[0]
            bs = bs+F_mul
print("BLEU1",corpus_bleu(r, c,weights=(1, 0, 0, 0))*100)
print("BLEU2",corpus_bleu(r, c,weights=(0, 1, 0, 0))*100)
print("BERTSCORE",float(bs)/150.0)
