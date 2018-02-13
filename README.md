# ML-tutorial  

Step1: separate tokens per article using tml_tokens_per_article.py  
Step2: extract tokens from tml_tokens, using tokens_for_Stanford_input.py  
Step3: Parse directory of text files from command line: java -cp "*" -mx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -tokenize.whitespace true -annotator depparse -filelist list_files.txt -outputFormat conll  
Step4: Remove spaces from Stanford output using:  
Step5: Merge all files to a single one using:  
