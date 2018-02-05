import pandas as pd

df_tokens = pd.read_csv('tml_tokens.txt', sep='\|', header= None).dropna(axis=1)

df_final = pd.read_csv('stanford_input.txt.conll', sep='\t', header= None)


df_final.columns = ["token_id", "token", "lemma", "POS", "0", "path", "dep"]
df_tokens.columns = ["article_id", "sentence_id", "token_id", "token", "na1", "na2", "na3"] #Sets headings
df_tokens["token"] = df_tokens["token"].str.replace("'", "") #This removes the apostrophes so that the tokens can match


df_tokens = df_tokens.drop(['article_id', 'na1', 'na2', 'na3'], 1)
print(df_tokens)


df_final = df_final.drop(["token_id", "0"], 1)
print(df_final)

#df_final = df_final.merge(df_tokens, axis=1) #Merges dataframes on 'token'

df_final = pd.concat([df_final, df_tokens], axis=1) #concatenates the dataframes


df_final = df_final.drop(["token"], 1) #removes duplicate token column

print('Final starts below')
print(df_final)

df_final.to_csv('preprocessed.csv', sep="\t") #writes to csv with tab as delimiter
