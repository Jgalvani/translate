
# coding: utf-8

import pandas as pd
from googletrans import Translator
from time import sleep
from tqdm import tqdm
from random import random

#Load english texts
df = pd.read_csv("../data/english_dataset.csv", index_col = False)

def try_translation(text):
    """try a translation using Google Translate API and wait between 1 and 60 seconds if the translation fails"""
    try:
        trad = Translator().translate(text = text, dest = 'fr')
    except:
        sleep(random() * 60)
        return False
    
    return trad.text

def trad_list(lst):
    trad_texts = list()
    
    for text in tqdm(lst, desc = 'text'):
        #split the text into sentences
        sentences = text.split('. ')
        trad_lst = list()
        
        for sentence in tqdm(sentences, desc = 'sentences'):
            #translate sentence by sentence
            trad = try_translation(sentence)

            while trad == False:
                trad = try_translation(sentence)
                
            trad_lst.append(trad)
        
        #turn the list of traductions into a string and save it in trad_texts
        trad_text = ". ".join(trad_lst)
        trad_texts.append(trad_text)
        del trad_lst
        del trad_text
        
    return trad_texts

df['french'] = trad_list(df['english'].tolist())

#save the result into a csv file
df.to_csv("../data/french_trad_english_dataset.csv", index = False)
