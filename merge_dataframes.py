import pandas as pd
import csv

#input files: fb_values, fb_events
fb_values = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/values1.txt'
fb_events = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/events2.txt'


def get_df_events(events_infile):
    """takes standoff file with events and returns a df with article, id, event_no, event_class, and token"""
    df_events = pd.read_csv(events_infile, sep='\|', header=None).dropna(axis=1)
    #Set headings
    df_events.columns = ["article", 'id', "event_no", "event_class",'token']
    #Remove the apostrophes so that the tokens can match
    df_events["token"] = df_events["token"].str.replace("'", "")
    #Remove the apostrophes so that the event_no can match
    df_events["event_no"] = df_events["event_no"].str.replace("'", "")
    
    return df_events

#assign df to variable
df_events = get_df_events(fb_events)


def get_df_values(values_infile):
    """takes standoff file with values and returns a df with sent_id, f_id, event_no, token, and f_value"""
    #make sure first row does not become header
    values_df = pd.read_csv(values_infile, sep='\|', header=None).dropna(axis=1)

    #set headings
    values_df.columns = ["article", 'sent_id', "f_id", "event_no", "ei_id", "source", 'token', 's_name', 'f_value']
    #Remove the apostrophes so that the tokens can match
    values_df["token"] = values_df["token"].str.replace("'", "")
    #Remove the apostrophes so that the f_id can match
    values_df["f_id"] = values_df["f_id"].str.replace("'", "")
    #Remove the apostrophes so that the event_no can match
    values_df["event_no"] = values_df["event_no"].str.replace("'", "")
    #Remove the apostrophes so that the f_value can match
    values_df["f_value"] = values_df["f_value"].str.replace("'", "")

    #Drop unwanted columns
    m_values_df = values_df.drop(['article','ei_id', 'source', 's_name'], 1)
    
    return m_values_df

#assign df to variable
all_values_df = get_df_values(fb_values)

#in order to access the values, create dictionary with event_no's as keys and factuality values as values
#since event_no's are not unique, I used "groupby" to collect in a list the values corresponding to the same event_no
#the factuality value corresponding to the least embedded source is always the first in the list of values in the dictionary
#create new dataframe with event_no's and f_values from dictionary
#create dictionary first
def get_df_wantedvalues(all_values_df):
    """Takes df with all values as input and outputs df with event_no and f_values """
    mydict_eventno = {k: g["f_value"].tolist() for k,g in all_values_df.groupby("event_no")}
    final_dict = {}
    for k, v in mydict_eventno.items():
        final_dict[k] = v[0]
    #transform final_dict into a dataframe
    wanted_values_df = pd.DataFrame(list(final_dict.items()),
                      columns=['event_no','f_value'])
    return wanted_values_df


def merge_dfs_events_values(df_events, df_wanted_values):
    """get merged df with events, event class, event_no, and wanted values"""
    merged_values_events = df_events.merge(df_wanted_values, on=['event_no'], how='left')
    
    return merged_values_events


#assign df to variable
df_wanted_values = get_df_wantedvalues(all_values_df)


#assign df to variable
df_events_wvalues = merge_dfs_events_values(df_events, df_wanted_values)


#output to tsv file
df_events_wvalues.to_csv('art_events_values_class.tsv', sep='\t')


#Obtain df from stanford ouput file
stan_output = '/Users/benedettatorsi/Downloads/stanford_input.txt.conll'


#file has a blank line separating the parse of each sentence
#first remove empty lines from conll file
def remove_blank_lines(stan_file):
    """functtion takes conll file, removes blank lines, outputs csv file with info from stanford parser"""
    with open(stan_file) as f:
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

    with open("stan_conllto.csv", "w") as f:
        w = csv.writer(f)
        w.writerows(split_lines)


#call function above to produce output
remove_blank_lines(stan_output)


#obtain df from stanford_csv file
stanford_csv = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/stan_conllto.csv'


def get_df_stan(stanford_csv):
    """takes csv file with with info from Stanford parser and outputs df with """
    df_stanf = pd.read_csv(stanford_csv, sep=',',header=None)

    df_stanf.columns = ["token_id", 'token', "lemma", "POS", "0", "head", 'dep'] #Sets headings
    df_stanf["dep"] = df_stanf["dep"].str.replace("\n", "") #This removes the '\n'
    #drop unwanted columns
    df_stanf = df_stanf.drop(['0'], 1)
    return df_stanf


#assign df to variable
df_stan = get_df_stan(stanford_csv)


#create column with indexing and set it as index
df_stan['index_col'] = df_stan.index


#Merge tokens file, event,class,value file, and stanford file via dataframe merging
#First get file with tokens and transform into df
infile_tokens = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/tml_tokens.txt'

#Obtain df from tokens file
def get_tokens_df(infile_tokens):
    """takes infile with tokens and returns a df with sent_id and tokens"""
    tokens_df = pd.read_csv(infile_tokens, sep='\|', header=None)
    #set headings
    tokens_df.columns = ['article', 'nan1', 'nan2', 'sent_id', 'nan3', 'nan4', 'number', 'nan5', 'nan6', 'token', 'nan7', 'nan8', 'timex', 'nan9', 'nan10', 't_or_ev', 'nan11', 'nan12', 'N']
    #drop columns
    df_tokens = tokens_df.drop(['nan1', 'nan2', 'nan3', 'nan4', 'number', 'nan5', 'nan6', 'nan7', 'nan8', 'timex', 'nan9', 'nan10', 't_or_ev', 'nan11', 'nan12', 'N'], 1)
    #Remove the apostrophes so that the tokens can match
    df_tokens["token"] = df_tokens["token"].str.replace("'", "")
    return df_tokens

#assign df to variable
df_tokens = get_tokens_df(infile_tokens)


#create column with indexing and set it as index
df_tokens['index_col'] = df_tokens.index

#merge all three datasets 
#first stanf and tokens
merged_stanf_tokens = df_tokens.merge(df_stan, on=['index_col'], how='left')
#merged_stanf_tokens = pd.merge_ordered(df_tokens, df_stan, left_on='index_col')

#set headings again
merged_stanf_tokens.columns = ["article", 'sent_id', "token", "index_col", "token_id", "token_y", "lemma", 'POS', 'head', 'dep'] #Sets headings
#drop unwanted column
merged_stanf_tokens = merged_stanf_tokens.drop(['token_y'], 1)

#Merge tokens and stanford outout with wanted events values file
everything_merge = merged_stanf_tokens.merge(df_events_wvalues, on="token", how="left")

#set headings again
everything_merge.columns = ['article', 'sent_id', 'token', 'ind', 'token_id', 'lemma', 'POS', 'head', 'dep', 'article_y', 'id', 'event_no', 'event_class', 'f_value', 'index_col_y']
#drop unwanted columns to obtain final dataframe
everything_merge = everything_merge.drop(['ind', 'article_y', 'id', 'event_no', 'index_col_y'], 1)

#output to tsv file
everything_merge.to_csv('stan_event_value.tsv', sep='\t')

