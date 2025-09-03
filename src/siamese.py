from utils.utils import *

import os
import re
import csv
import codecs

import numpy as np
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow
import keras
import pickle

from keras.models import Model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

############ LOADING MODELS ############
model = keras.models.load_model('utils/models/main.h5')

with open('utils/models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
############ LOADING MODELS ############


def get_similarity(TEST_DATA_FILE = 'utils/temp.csv'):

    test_texts_1 = []
    test_texts_2 = []
    test_ids = []
    with codecs.open(TEST_DATA_FILE) as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        for values in reader:
            try:
              test_texts_1.append(text_to_wordlist(values[1]))
              test_texts_2.append(text_to_wordlist(values[2]))
              #print(test_texts_1)
              #print(test_texts_2)
              test_ids.append(values[0])
            except:
              print('Didnt Reach Block')

    test_sequences_1 = tokenizer.texts_to_sequences(test_texts_1)
    test_sequences_2 = tokenizer.texts_to_sequences(test_texts_2)

    word_index = tokenizer.word_index

    MAX_SEQUENCE_LENGTH = 30

    test_data_1 = pad_sequences(test_sequences_1, maxlen=MAX_SEQUENCE_LENGTH)
    test_data_2 = pad_sequences(test_sequences_2, maxlen=MAX_SEQUENCE_LENGTH)
    test_ids = np.array(test_ids)

    #print(test_data_1)
    #print(test_data_2)

    #preds = 0
    preds = model.predict([test_data_1, test_data_2], batch_size=8192, verbose=1)
    preds += model.predict([test_data_2, test_data_1], batch_size=8192, verbose=1)
    preds /= 2
    #print(preds)

    if preds<0.09:
        preds = preds * 1000
    else:
        preds = preds * 100

    return preds

if __name__=='__main__':

    get_similarity(TEST_DATA_FILE = 'utils/test-20c.csv')
