for SPLIT in train val
do
  for LANG in source target
  do
    python -m examples.roberta.multiprocessing_bpe_encoder \
    --encoder-json encoder.json \
    --vocab-bpe vocab.bpe \
    --inputs "simile/$SPLIT.$LANG" \
    --outputs "simile/$SPLIT.bpe.$LANG" \
    --workers 60 \
    --keep-empty;
  done
done
