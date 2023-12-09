import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from IPython.display import HTML

def getDataset(data):
    if data == "Huffingpost":
        data1 = pd.read_json('dataset_f\Sarcasm_Headlines_Dataset_v2.json',lines=True)
        data1.drop('article_link', axis=1, inplace=True)
        d1 = data1['is_sarcastic']
        return data1
    elif(data == "Times of India"):
        data1 = pd.read_pickle('dataset_f\saved_dataframe.pkl')
        data1.drop('publish_date',inplace=True, axis = 1)
        data1.columns.values[0:1] =["headline"]
        d1 = data1['is_sarcastic']
        return data1
    elif(data == "BBC News"):
        data1 = pd.read_pickle('dataset_f\saved_dataframe2.pkl')
        #data1.drop('publish_date',inplace=True, axis = 1)
        data1.columns.values[0:1] =["headline"]
        d1 = data1['headline']
        return data1
    
    

#This is used for data display of suitable news Data
def retData(data):
    if data == "Huffingpost":
        data1 = pd.read_json('dataset_f\Sarcasm_Headlines_Dataset_v2.json',lines=True)
        data1.drop('article_link', axis=1, inplace=True)
        data_1= data1.head(6)
        return data_1
    elif(data == "Times of India"):
        data1 = pd.read_pickle('dataset_f\saved_dataframe.pkl')
        data1.drop('publish_date',inplace=True, axis = 1)
        data1.columns.values[0:1] =["headline"]
        data_1= data1.head(6)
        return data_1
    elif(data == "BBC News"):
        data1 = pd.read_pickle('dataset_f\saved_dataframe2.pkl')
        #data1.drop('publish_date',inplace=True, axis = 1)
        data1.columns.values[0:1] =["headline"]
        data_1= data1.head(6)
        return data_1
    
# convHtml this function is for converting dataframe to html table
# Reason to directly display in table no need to extract from dataset

def convHtml(data2):
    data_2 = data2.to_html()
    data_2 = data_2.replace('<table border="1" class="dataframe">','<table class="table table-striped">')
    text_file = open("application/templates/index3.html", "w")
    text_file.write(data_2)
    text_file.close()
    

# Function for the count of sarcastic and non sarcastic headlines 
def GetSarc_count(data,value1):
    if data == "Huffingpost":
        data1 = pd.read_json('dataset_f\Sarcasm_Headlines_Dataset_v2.json',lines=True)
        data1.drop('article_link', axis=1, inplace=True)
        sarc = data1['is_sarcastic'].value_counts()[value1]
        return sarc
    elif(data == "Times of India"):
        data1 = pd.read_pickle('dataset_f\saved_dataframe.pkl')
        data1.drop('publish_date',inplace=True, axis = 1)
        data1.columns.values[0:1] =["headline"]
        sarc = data1['is_sarcastic'].value_counts()[value1]
        return sarc
    elif(data == "BBC News"):
        data1 = pd.read_pickle('dataset_f\saved_dataframe2.pkl')
        #data1.drop('publish_date',inplace=True, axis = 1)
        data1.columns.values[0:1] =["headline"]
        sarc = data1['is_sarcastic'].value_counts()[value1]
        return sarc
   