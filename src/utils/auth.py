import os,io
from google.cloud import vision
#from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'capstone1057-a58de951c739.json'

client = vision.ImageAnnotatorClient()
