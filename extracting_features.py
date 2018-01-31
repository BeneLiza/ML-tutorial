import pandas as pd

df = pd.read_csv('ML1_events.txt', sep='\|', header=0).dropna(axis=1)

df2 = pd.read_csv('ML1.txt.conll', sep='\t')



df2.columns = [" id", "token", "lemma", "pos", "_", "path", "dep"] #Sets headings
df.columns = ["article", "number", "event_no", "event_class", "token"] #Sets headings
df["token"] = df["token"].str.replace("'", "") #This removes the apostrophes so that the tokens can match

print(df)
print("Dataframe 2 starts here")
print(df2)

merged_df = df2.merge(df, on=['token'], how='left') #Merges dataframes on 'token'

print("Merged df starts here")
print(merged_df)

merged_df = merged_df.drop(['article', 'number','event_no'], 1) #Drops unwanted columns

print('final merged_df here')
print(merged_df)

merged_df.to_csv('merged_df.csv')