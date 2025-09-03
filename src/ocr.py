from utils.utils import *
import os,io
from google.oauth2 import service_account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'utils/capstone1057-a58de951c739.json'

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        PER_BLOCK = []
        for block in page.blocks:
            #print('\nBlock confidence: {}\n'.format(block.confidence))
            for paragraph in block.paragraphs:
                #print('Paragraph confidence: {}'.format(
                    #paragraph.confidence))
                #print(paragraph.words)
                s = ''
                PER_PARA = []

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    #print(word_text)
                    PER_PARA.append(word_text)

                for word in PER_PARA:
                    s = s + word + ' '
                #print(s)
                PER_BLOCK.append(s)
        #print(PER_BLOCK)
        s = ''
        for sentence in PER_BLOCK:
            s = s + sentence + ' '
        #print(s)
        #print('\n')

        s = spell_check(s)
        #print(s)
        return s


        '''
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))
        '''

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


if __name__=="__main__":


    #print('##### WITHOUT PRE-PROCESS #####')
    detect_document('PHOTOS/example3.jpg')
    #print('##### WITHOUT PRE-PROCESS #####\n')
