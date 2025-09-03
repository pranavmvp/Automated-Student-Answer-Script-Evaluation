import os
import cv2

from crop import *
from ocr import *
from utils.utils import *
from utils.preset import *
from siamese import *
from nlp import *

#print(os.listdir())

# Get images in list
ROOT = 'PHOTOS'
IMAGES = ['example3']

for img in IMAGES:

    # Reading Each Image
    PATH = ROOT + '/' + img + '.jpg'
    initial = cv2.imread(PATH)

    '''
    # Crop Image via Object Detection
    cropped = localize_objects(PATH, initial)
    SAVED = ROOT + img + '_cropped' + '.jpg'
    cv2.imwrite(SAVED, cropped)
    '''
    SAVED = PATH

    # Pass refined image to OCR Function and perform spell check
    #answer = detect_document(SAVED)
    answer = get_post()
    print('###################### ANSWER ######################')
    print(answer)
    print('###################### ANSWER ######################\n')

    # Loading presets
    print('###################### PRESET ######################')
    query = load_query()
    print(query[1])
    print('###################### PRESET ######################\n')

    # Add preset and answer to a dataframe
    create_csv(query[1], answer)

    # Get multiplier based on keywords, phrases
    ST_Multiplier, NON_ST_Multiplier = get_multiplier(query[1], answer)
    Phrases = n_grams(query[1], answer)

    # Get Similarity Score
    Score = get_similarity()
    Score = Score[0][0]

    print('\nBase Similarity Score = ',Score, '%')
    print('Multiplier % : ',ST_Multiplier)
    print('Phrases : ', Phrases)
    if ST_Multiplier!=0:
        Score = Score + (ST_Multiplier/2)*100
        Score = Score + Phrases/2

        if Score>100:
            Score = 99.99

    else:
        print('Error with keyword matching. None found. ')

    #print('Matching Phrases = ',Phrases)
    print('\n########################################')
    print('Final Score = ',Score, ' %')
    print('########################################')

    # Evaluate and display final scores
    '''
    1) Min length of the answer
    '''
