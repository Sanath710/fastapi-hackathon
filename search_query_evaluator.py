
# coding: utf-8

# ### **Required Dependencies**

# In[186]:


# !pip install googletrans==3.1.0a0
# !pip install rake-nltk


# In[187]:


import json, nltk, string, pandas as pd, os, re, enchant
from rake_nltk import Rake
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
from googletrans import Translator as tns


# In[188]:


#nltk.download('stopwords')


# ### **Language Transformation**

# In[189]:


def lang_transform(query) :
    translator = tns()
    return translator.translate(query, dest="en").text


# ### **Key Term Extraction**

# In[190]:


# stop_words = stopwords.words("english")
# lemmatizer = WordNetLemmatizer()
# key_terms = [lemmatizer.lemmatize(t) for t in transformed_query.split() if t not in stop_words and t not in string.punctuation and len(t) > 2]
# print("Query : ", transformed_query, "\nKey Terms : ", key_terms)

def search(query) :
    transformed_query = lang_transform(query)

    rake = Rake()
    rake.extract_keywords_from_text(transformed_query)
    keywords_extracted = rake.get_ranked_phrases()
    
    return keywords_extracted, transformed_query


# ### **Data Munging & Visualization**

# In[191]:


file = os.path.join(os.getcwd(),"first-aid_dataset","dataset.json")

dataset = json.load(open(file))

# dataset = None
# with open(file, 'r') as f:
#     dataset = json.loads(f.read())


# In[192]:


dataframe = pd.DataFrame.from_dict(dataset["intents"])


# In[193]:


dataframe.drop(columns="context_set", inplace=True) # Empty Useless
# dataframe.rename(columns = {"tag":"symptoms"}, inplace=True)


# In[194]:


# dataframe.shape


# In[195]:


# dataframe.columns


# In[196]:


# dataframe.info()


# In[197]:


dataframe.tag = [str(n).lower() for n in dataframe.tag]
dataframe.patterns = [str(n).lower() for n in dataframe.patterns]


# In[198]:


# dataframe


# In[199]:


# Empty Checks
cnt = 0
for r in dataframe["responses"].values :
    if " " in r : cnt += 1
        
# print("Empty Rows \t: ", cnt, "\nNon-Empty Rows  : ",len(dataframe.responses)-cnt,"\nTotal Rows \t: ",len(dataframe.responses))


# In[200]:


tags = list(dataframe.tag)
patterns = list(dataframe.patterns)
#tags


# In[229]:


def search_results(query) :
    
    d = dict()
#     greets = ["Hi", "Hello", "Hey"]
    
#     if query in greets :
#         return "Greet_initiate" : "Hello, ACE here.\nHow can I help you ?"
    
    keywords, transformed_query = search(query)
    global tags, patterns, dataframe
    
    for t, p in zip(tags, patterns) :
        for kwrd in keywords :
            if re.findall(kwrd, t) or re.findall(t,kwrd) :
                d[t] = {"question" : dataframe[dataframe.tag == t].patterns.tolist(), "response" : dataframe[dataframe.tag == t].responses.tolist(), "transformed_query" : transformed_query}
    
    if d.keys() : 
        d["Greet_terminate"] = "Have a fast recovery & healthy hygiene.\nIf you are not satisfied with the response text me HELP"
        return json.dumps(d)
    else :
        """
        keywords = []
        
        d = enchant.Dict("en_US")
        
        for w in query.split(" ") :
            if d.check(w) : keywords.append(w)
        #print(keywords)
 
        temp = {}
        for t, p in zip(tags, patterns) :
            for kwrd in keywords :
                if re.findall(kwrd, t) or re.findall(t, kwrd) :
                    temp[t] = {"question" : dataframe[dataframe.tag == t].patterns.tolist(), "response" : dataframe[dataframe.tag == t].responses.tolist(), "transformed_query" : transformed_query}

        if temp .keys() : 
            temp["Greet_terminate"] = "Have a fast recovery & healthy hygiene.\nIf you are not satisfied with the response text me HELP"
            return json.dumps(temp)
        
        d["Greet_terminate"] = "Have a fast recovery & healthy hygiene.\nIf you are not satisfied with the response text me HELP"
        """
        return {"err":"Sorry, I didn't understood what you are saying.!"}

    
def initiate_ACE(query) :
    try :
        #query = input("Search : ")
        return search_results(query)
    except :
        return {"err":"Sorry, I didn't understood what you are saying.!"}
# In[228]:


#query = input("Search : ")
#search_results(query)

# search_results("mane mathu dukhe sathe khasi bhi che")

