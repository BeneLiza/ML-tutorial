
# coding: utf-8

# In[5]:


#import files: events,class,value   tokens file    conll file 
infile_event_class_value = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/events_values_class.tsv'
infile_conll = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/stanford_input.txt.conll'
infile_tokens = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/tml_tokens.txt'


# In[4]:


import pandas as pd


# In[43]:


#### get dataframes for all of the above files
## first remove empty lines from conll file
with open(infile_conll) as f:
    lines = f.readlines()
    lines_nb = []
    for i in lines:
        if i != '':
            if i != '\n':
                lines_nb.append(i)
split_lines = []
for i in lines_nb:
    line = i.split('\t')
    split_lines.append(line)

with open("conllto.csv", "w") as f:
    w = csv.writer(f)
    w.writerows(split_lines)
    


# In[44]:


infile_csv_conll = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/conllto.csv'


# In[47]:


#get dataframes
#conll file
df_stanf = pd.read_csv(infile_csv_conll, sep=',',header=None)


# In[49]:


#set headings, modify content columns
df_stanf.columns = ["token_id", 'token', "lemma", "POS", "ev_class", "path", 'dep'] #Sets headings
df_stanf["dep"] = df_stanf["dep"].str.replace("\n", "") #This removes the '\n'


# In[51]:


#event_class_value file
ev_cl_val_df = pd.read_csv(infile_event_class_value, sep='\t')


# In[64]:


#set headings
ev_cl_val_df.columns = ['id', 'article', 'number', 'event_no', 'event_class', 'token', 'number_1', 'f_value']
#drop columns
ev_cl_val_df = ev_cl_val_df.drop(['id', 'article', 'number', 'number_1'], 1)


# In[60]:


#tokens file 
tokens_df = pd.read_csv(infile_tokens, sep='\|', header=None)


# In[67]:


#set headings
tokens_df.columns = ['article', 'nan1', 'nan2', 'sent_id', 'nan3', 'nan4', 'number', 'nan5', 'nan6', 'token', 'nan7', 'nan8', 'timex', 'nan9', 'nan10', 't_or_ev', 'nan11', 'nan12', 'N']
#drop columns
tokens_df = tokens_df.drop(['article', 'nan1', 'nan2', 'nan3', 'nan4', 'number', 'nan5', 'nan6', 'nan7', 'nan8', 'timex', 'nan9', 'nan10', 't_or_ev', 'nan11', 'nan12', 'N'], 1)


# In[70]:


#merge all three datasets 
#first stanf and tokens
merged_stanf_tokens = df_stanf.merge(tokens_df, on=['token'], how='left')


# In[72]:


#then with class and value
final_merged = merged_stanf_tokens.merge(ev_cl_val_df, on=['token'], how='left')


# In[74]:


#output to tsv
final_merged.to_csv('everything_merged.tsv', sep='\t')

