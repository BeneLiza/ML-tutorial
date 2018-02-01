
# coding: utf-8

# In[1]:


infile = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/values1.txt'


# In[119]:


infile_events = '/Users/benedettatorsi/Documents/Machine_Learning/ML_tutorial/events1.txt'


# In[118]:


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# In[177]:


#checking number of events in file with event_no's and tokens
file_len(infile_events)


# In[176]:


#obtaining a dataframe from file with factuality values
import pandas as pd

df = pd.read_csv(infile, sep='\|', header=None).dropna(axis=1)


# In[11]:


print(df)


# In[29]:


df.columns = ["article", 'sent_id', "f_id", "event_no", "ei_id", "source", 'token', 's_name', 'f_value'] #Sets headings
df["token"] = df["token"].str.replace("'", "") #This removes the apostrophes so that the tokens can match
df["f_id"] = df["f_id"].str.replace("'", "") #This removes the apostrophes so that the tokens can match
df["event_no"] = df["event_no"].str.replace("'", "") #This removes the apostrophes so that the tokens can match
df["f_value"] = df["f_value"].str.replace("'", "") #This removes the apostrophes so that the tokens can match


# In[30]:


modified_df = df.drop(['article','ei_id', 'source', 's_name'], 1) #Drops unwanted columns


# In[178]:


#experimenting with dataframe, you can ignore this
df2=modified_df.set_index("event_no")


# In[180]:


#trying one strategy where I construct a nested dictionary with the information I need, YOU CAN IGNORE THIS
##PLAN
#dictionary = {f17: {e18: ct+}
#{f18: {e18: uu}

#in dictionary
#if key within key is the same, if key is smaller than other key then get the value 

#do dictionary within dictionary
#get dictionary with f_id as key and f_id as value event_no and f_value so that you can see if the e_no is the same, then get


# In[181]:


#test YOU CAN IGNORE THIS
dic = {'f17': {'e18': 'CT+'}, 'f18':{'e18': 'Uu'}}  


# In[182]:


#writing functions to execute above-mentioned steps YOU CAN IGNORE THIS
def get_int_ind(dic):
    """returns a list of dictionaries with integers as keys"""
    list_dic = []
    for key, value in dic.items():
        dic1 = {}
        #removing 'f' and tranforming number to an int so that later we can access the lowest integer
        key1 = int(key.strip('f'))
        dic1[key1] = value
        list_dic.append(dic1)
    return list_dic


# In[183]:


list_dic = get_int_ind(dic)


# In[184]:


#YOU CAN IGNORE THIS
def get_min_int(list_dic):
    """gets the the dictionary with the lowest integer as key"""
    list_k = []
    #value_list = []
    for item in list_dic:
        for k, v in item.items():
            list_k.append(k)
            x = min(float(s) for s in list_k)
        for k, v in item.items():
            if k == x:
                return item


# In[185]:


#YOU CAN IGNORE THIS
value_list = get_min_int(list_dic)
print(value_list)


# In[186]:


#YOU CAN IGNORE THIS
test = 'f17'
test1 = int(test.strip('f'))
#print(type(test1))

def get_int_ind(dic):
    list_dic = []
    for key, value in dic.items():
        dic1 = {}
        key1 = int(key.strip('f'))
        dic1[key1] = value
        list_dic.append(dic1)
    return list_dic
    
print(list_dic)
list_k = []
for item in list_dic:
    for k, v in item.items():
        list_k.append(k)
        x = min(float(s) for s in list_k)
        
value_list = []
for item in list_dic:
    for k, v in item.items():
        if k == x:
            value_list.append(item)

print('wanted value', value_list)    
print('list', list_k)
print(x)


# In[187]:


#YOU CAN IGNORE THIS
#create a dictionary with f_id's as keys and event_no's as values 
#f_id's are unique so they work as keys, event-no's are not so they work as values
mydict_fid = modified_df.set_index('f_id')['event_no'].to_dict()
print(mydict_fid)


# In[112]:


####This is the strategy I want to end up using
#in order to access the values, create dictionary with event_no's as keys and factuality values as values
#since event_no's are not unique, I used "groupby" to collect in a list the values corresponding to the same event_no
mydict_eventno = {k: g["f_value"].tolist() for k,g in modified_df.groupby("event_no")}
print(mydict_eventno)


# In[189]:


#note how the factuality value corresponding to the least embedded source is always the first in the list in the above dictionary
#here are the things I'm interested in: event_no's and the first f_value in the list
#event_no1 = #keys in mydict_eventno
#f_value = #[0] in value in mydict_eventno


# In[208]:


###Now I would like to start building the final dataframe
#I use the dictionary mydict_eventno to build a dataframe
#Since we now have only one factuality value and one event_no per event
#the number of rows would not match with the number of rows contained in modified_df
#So I'm taking a different file which only contains events (no values upon which the duplication of the tokens and event_no's is based)
#Infile_events has the same # of rows as the two dataframes we obtained from the two dictionaries


# In[204]:


#transform file with events into a dataframe
df_ev = pd.read_csv(infile_events, sep='\|', header=None).dropna(axis=1)

df_ev


# In[205]:


df_ev.columns = ["article", 'id', "event_no", "ei_id",'token'] #Sets headings
df_ev["token"] = df_ev["token"].str.replace("'", "") #This removes the apostrophes so that the tokens can match
df_ev["event_no"] = df_ev["event_no"].str.replace("'", "") #This removes the apostrophes so that the tokens can match


# In[206]:


modified_df_ev = df_ev.drop(['article','ei_id', 'id'], 1) #Drops unwanted columns


# In[207]:


#53 rows
modified_df_ev


# In[198]:


#create new dataframe with event_no's and f_values from dictionary
final_dict = {}
for k, v in mydict_eventno.items():
    final_dict[k] = v[0]


# In[199]:


#checking number of rows
print(len(final_dict))


# In[200]:


#transform final_dict into a dataframe
final_dataframe = pd.DataFrame(list(final_dict.items()),
                      columns=['event_no','f_value'])
print(len(final_dataframe))


# In[209]:


#merge final_dataframe and modified_df_ev
merged_df3 = final_dataframe.merge(modified_df_ev, on=['event_no'], how='left') #Merges dataframes on 'event_no'
print(len(merged_df3))


# In[212]:


#creating outfile
merged_df3.to_csv('events_values.csv')

