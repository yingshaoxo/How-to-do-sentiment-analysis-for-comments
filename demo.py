from os import listdir
from os.path import isfile, join
from pprint import pprint
from auto_everything.base import IO
io = IO()

import jieba
import codecs
import pickle
import random

from keras.models import load_model
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import GRU
from keras.preprocessing.text import Tokenizer
from keras.layers.core import Dense
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences

import numpy as np



def __pickleStuff(filename, stuff):
    save_stuff = open(filename, "wb")
    pickle.dump(stuff, save_stuff)
    save_stuff.close()
    
def __loadStuff(filename):
    saved_stuff = open(filename,"rb")
    stuff = pickle.load(saved_stuff)
    saved_stuff.close()
    return stuff



metaData = __loadStuff("./data/meta_sentiment_chinese.p")
maxLength = metaData.get("maxLength")
vocab_size = metaData.get("vocab_size")
output_dimen = metaData.get("output_dimen")
sentiment_tag = metaData.get("sentiment_tag")

def loadModel():
    model = load_model('./data/sentiment_chinese_model.H5')
    print("Model loaded!")
    return model

def findFeatures(text):
    seg_list = jieba.cut(text, cut_all=False)
    seg_list = list(seg_list)
    text = " ".join(seg_list)
    textArray = [text]
    input_tokenizer_load = __loadStuff("./data/input_tokenizer_chinese.p")
    textArray = np.array(pad_sequences(input_tokenizer_load.texts_to_sequences(textArray), maxlen=maxLength))
    return textArray

def predict(text):
    if model is None:
        print("Please run \"loadModel\" first.")
        return None
    features = findFeatures(text)
    predicted = model.predict(features)[0] # we have only one sentence to predict, so take index 0
    predicted = np.array(predicted)
    probab = predicted.max()
    predition = sentiment_tag[predicted.argmax()]
    return predition, probab


model = loadModel()

import time
from auto_everything.web import Selenium
my_selenium = Selenium("https://baidu.com")
driver = my_selenium.driver

print('\n'*12)
while True:
    url = input("请输入你想要分析的网站url: ")
    if url.strip('\n ') == "":
        continue

    driver.get(url)
    driver.execute_script("window.scrollBy(0,40000)")
    time.sleep(1)
    elements = my_selenium.wait_until_exists('//div') # //p

    for e in elements:
        try:
            text = e.text.strip('\n ')
            if text != "":
                r = predict(text)
                print(text, '\n', r, '\n'*2)
                if r[0] == "pos":
                    #time.sleep(3)
        except Exception as e:
            print(e)
