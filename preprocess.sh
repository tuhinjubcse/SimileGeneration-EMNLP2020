fairseq-preprocess \
  --source-lang "source" \
  --target-lang "target" \
  --trainpref "simile/train.bpe" \
  --validpref "simile/val.bpe" \
  --destdir "simile/" \
  --workers 60 \
  --srcdict dict.txt \
  --tgtdict dict.txt;
