# ML-tutorial

Step1: extract tokens from tml_tokens, using tokens_for_Stanford_input.py
Step2: Command line usage: java -cp "\*" -mx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -tokenize.whitespace true  -annotator depparse  -file stanford_input.txt -outputFormat conll
Step3: Combine data sources into one .tsv using ___
