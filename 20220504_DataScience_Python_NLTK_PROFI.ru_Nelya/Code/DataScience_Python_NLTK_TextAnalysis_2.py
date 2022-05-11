#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Task description:
#У меня есть 985 комментариев о работе компании и пожеланиях клиентов. 
#1. Нужно получить коэффициенты сентиментов по каждому, то есть насколько комментарий 
#положительный или отрицательный. 
#2. Также желательно определить, к каким отделам относятся 
#эти комментарии, чтобы понять, кому их надо брать в работу. 
#3. Задача максимум: ещё и связать 
# коэффициенты сентиментов с количественными оценками, которые клиенты выставляли по 
# отдельным критериям работы компании. Вы такое умеете делать?


# In[45]:


import pandas as pd #импорт модуля пандас под именем пд, необходимого для работы с таблицей из экселя
from string import punctuation #импорт объекта для удаления знаков препинания между словами
import os.path

# English language
import nltk #импорт пакета nltk для NLP
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords #импорт объекта для удаления лишних (стоп) слов из модуля corpus из пакета nltk для NLP

nltk.download([
    "punkt",
    "stopwords",
])

#Russian language
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel


# In[53]:


def setup(path: str = os.path.abspath(input("Enter path of your Excel document: "))):
    try:
         return pd.read_excel(path,usecols='A,J') #выбираем только колонки A, J для идентификации и анализа
    except OSError:
        if not os.path.isfile(path):
            print("Excel document isn't exist")


# In[54]:


survey = setup("/Users/lucifer/Desktop/20220504_DataScience_Python_NLTK_PROFI.ru_Nelya/Excel2.xlsx")


# In[55]:


def GetDataFromDocByKey(document: list, key: str) -> list:
    if len(document) == 0:
        raise ValueError('Argument empty', type(document))
        
    if len(key) == 0:
        raise ValueError('Argument empty', type(key))  
    
    return document[key].astype(str).tolist()

comments = GetDataFromDocByKey(survey, "Комментарий клиента") #создаем массив только с комментариями
clientsIds = GetDataFromDocByKey(survey, "Id шаблона") #создаем массив только с id клиента 


# In[56]:


# TODO: It isn't best code it should be ovewrited to follow SOLID principles  
def matchrus(text: str, alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')) -> bool:
    return not alphabet.isdisjoint(text.lower()) #функция для проверки, если комментарий написан на русском

# TODO: It isn't best code it should be ovewrited to follow SOLID principles 
def matcheng(text: str, alphabet = set('abcdefghijklmnopqrstuvwxyz')) -> bool:
    return not alphabet.isdisjoint(text.lower()) #функция для проверки, если комментарий написан на английском
    # x - 'a' >= 0 && x - 'a' <= 26


# In[94]:


def GetCommentsRusOrEng(clientsIds: list, comments: list) -> list:
    if len(clientsIds) == 0:
        raise ValueError('Argument empty', type(clientsIds))
        
    if len(comments) == 0:
        raise ValueError('Argument empty', type(comments))
    
    russiancomments = [] # создаем три пустых массива, чтобы в них записать, соответственно, комментарии на русском
    englishcomments = [] # на английском
    nulcomments = [] # и "нулевые"
    
    for i in range(0, len(clientsIds)): #цикл, который исполняется для каждого id клиента
        #array = [] #пустой массив
        #array.append(i) #в него записываем порядковый номер строки, начиная с 0
        #array.append(clientsIds[i]) #следом в него записываем id клиента
        #array.append(comments[i]) #и его комментарий
        
        comment = comments[i]

        # TODO: I think it's possible to move the check to a separate method
        if matchrus(comment):
            russiancomments.append(comment) #если комментарий на русском, записываем в массив для руссских комментариев
        elif matcheng(comment):
            englishcomments.append(comment) #аналогично для английского
        else:
            nulcomments.append(comment) #оставшиеся попадают в "нулевой" массив
            
    return russiancomments, englishcomments, nulcomments


# In[95]:


russiancomments, englishcomments, nulcomments = GetCommentsRusOrEng(clientsIds, comments)


# In[96]:


def PrintComments(comments: list, lang: str) -> None:
    if len(comments) == 0:
        raise ValueError('Argument empty', type(comments))
        
    if len(lang) == 0:
        raise ValueError('Argument empty', type(lang))
    
    print(f"{lang} comments", comments)
    
#получился массив в массиве на самом деле, но для простоты понимания ниже буду называть массивы в массиве строчками
PrintComments(russiancomments, "Russia")
PrintComments(englishcomments, "English")
PrintComments(nulcomments, "Nul")

print("Amount of Russia comments: ", len(russiancomments)) #печатаем количество строк в каждом массиве
print("Amount of English comments: ", len(englishcomments)) #так их можно сложить и ерепроверить, что сумма сошлась верно
print("Amount of Nul comments: ", len(nulcomments)) #можно это и булевой функцией записать коротко, но пока нужна наглядность для корректировки


# In[97]:


def GetStopwords(lang: str) -> list:
    if len(lang) == 0:
        raise ValueError('Argument empty', type(lang))
    
    return stopwords.words(lang)

russian_stopwords = GetStopwords("russian")
print(russian_stopwords) #печатаем русские лишние (стоп) слова из пакета nltk, чтобы понимать, что будем дальше выкидывать

english_stopwords = GetStopwords("english")
print(english_stopwords) #для английского отдельно


# In[98]:


def GetTokensOrWords(comments: list, stopwords = None, punctuation = None) -> []:
    if len(comments) == 0:
        raise ValueError('Argument empty', type(comments))
    
    if stopwords is not None and len(stopwords) == 0:
        raise ValueError('Argument empty', type(stopwords))
        
    if punctuation is not None and len(punctuation) == 0:
        raise ValueError('Argument empty', type(punctuation))
    
    tokens = []
    
    for i in range(0, len(comments)): #делим тексты на токены, то есть на отдельные слова, выкидывая знаки препинания и стоп-слова
        #text = comments[i][2] # jagged array
        text = comments[i]
        tokens = nltk.word_tokenize(text.lower())
        if stopwords is not None and punctuation is not None:
            tokens = [token for token in tokens if token not in stopwords and token not in punctuation]
    return tokens


# In[99]:


russianWords = GetTokensOrWords(russiancomments, russian_stopwords, punctuation)
englishWords = GetTokensOrWords(englishcomments, english_stopwords, punctuation)
nulWords = GetTokensOrWords(nulcomments)


# In[111]:


print ("Russian words", russianWords)
print ("English words", englishWords)
print ("Nul words", nulWords)


# In[171]:


def comment_is_positive(sia, comment: str) -> bool:
    if sia is None:
        raise ValueError('Argument empty', type(sia))
    
    if len(comment) == 0:
        raise ValueError('Argument empty', type(comment))
        
    """True if comment has positive compound sentiment, False otherwise."""
    #return sia.polarity_scores(comment)["compound"] > 0 # negate 0-1, neural 0-1, postive 0-1, compound 0-1
    if type(sia) == "nltk.sentiment.vader.SentimentIntensityAnalyzer":
        return sia.polarity_scores(comment)["compound"] > 0
    if type(sia) == "<class 'dostoevsky.models.FastTextSocialNetworkModel'>":
        #sentiment = sia.predict(comment)
        
        #neutral = sentiment.get('neutral')
        #negative = sentiment.get('negative')
        #positive = sentiment.get('positive')
        
        #return ((neutral + negative + positive) / 3) > 0
        raise NotImplementedError(f"Can't use analyzer {type(sia)}")

def PrintSentiments(sia, comments: list) -> None:
    if sia is None:
        raise ValueError('Argument empty', type(sia))
    
    if len(comments) == 0:
        raise ValueError('Argument empty', type(comments))
    
    for comment in comments:
        print(">", comment_is_positive(sia, comment), comment)
    #for kv_comment in comments:
        #value = kv_comment[2]
        #print(">", comment_is_positive(value), value)

def SentimentAnalyses(comments: list, lang: str = "Eng") -> None:
    if len(comments) == 0:
        raise ValueError('Argument empty', type(comments))
    
    if len(lang) == 0:
        raise ValueError('Argument empty', type(lang))
    
    if lang == "Russian" or lang == "Rus":
        tokenizer = RegexTokenizer()
        FastTextSocialNetworkModel.MODEL_PATH = '/Users/lucifer/Desktop/20220504_DataScience_Python_NLTK_PROFI.ru_Nelya/fasttext-social-network-model.bin'
        sia = FastTextSocialNetworkModel(tokenizer=tokenizer)        
        PrintSentiments(sia, comments)

        #for comment, sentiment in zip(comments, results):
            #print(comment, '->', sentiment)

    if lang == "English" or lang == "Eng":
        sia = SentimentIntensityAnalyzer()
        PrintSentiments(sia, comments)


# In[170]:


SentimentAnalyses(russiancomments, "Rus")


# In[153]:


tokenizer = RegexTokenizer()
FastTextSocialNetworkModel.MODEL_PATH = '/Users/lucifer/Desktop/20220504_DataScience_Python_NLTK_PROFI.ru_Nelya/fasttext-social-network-model.bin'
sia = FastTextSocialNetworkModel(tokenizer=tokenizer)
sentiments = sia.predict(russiancomments)


# In[157]:


for comment, sentiment in zip(russiancomments[:3], sentiments[:3]):
    print(comment, '->', sentiment)


# In[148]:


tokenizer.split(russiancomments[0])


# In[143]:


for message, sentiment in zip(comment, sentiments):
    # привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
    # люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
    # малолетние дебилы -> {'negative': 0.9525841474533081, 'neutral': 0.13661839067935944}]
    print(message, '->', sentiment)


# In[15]:


#from dostoevsky.tokenization import RegexTokenizer
#from dostoevsky.models import FastTextSocialNetworkModel
#import wget 
#from fasttext import load_model

#tokenizer = RegexTokenizer()
#tokens = tokenizer.split('всё очень плохо')  # [('всё', None), ('очень', None), ('плохо', None)]

FastTextSocialNetworkModel.MODEL_PATH = '/Users/lucifer/Desktop/20220504_DataScience_Python_NLTK_PROFI.ru_Nelya/fasttext-social-network-model.bin'
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

messages = [
    'привет',
    'я люблю тебя!!',
    'малолетние дебилы'
]

results = model.predict(messages, k=2)

for message, sentiment in zip(messages, results):
    # привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
    # люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
    # малолетние дебилы -> {'negative': 0.9525841474533081, 'neutral': 0.13661839067935944}]
    print(message, '->', sentiment)


# In[ ]:




