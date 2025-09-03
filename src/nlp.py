import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words("english")
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def keywords(text,x):

    # Convert to Tokens
    tokens = nltk.word_tokenize(text)
    #print(tokens, '\n')

    # Convert to lower and remove non-alphabets
    lower = [ word.lower() for word in tokens if word.isalpha()]
    #print(tokens2, '\n')

    # Remove stopwords
    keywords = [word for word in lower if word not in stop_words]
    #print(keywords, '\n')

    # Lemmatize w.r.t nouns and then verbs
    temp = [lemmatizer.lemmatize(word, pos='n') for word in keywords]
    keyword_lemma = [lemmatizer.lemmatize(word, pos='v') for word in temp]
    #print(x,keyword_lemma)

    return keywords, keyword_lemma

def get_multiplier(question, answer):

    q_keyword, q_keyword_lemma = keywords(question,'Question Keywords = ')
    a_keyword, a_keyword_lemma = keywords(answer, 'Answer Keywords = ')

    keyword_set=set.intersection(set(a_keyword),set(q_keyword))
    #print('\nKeyword Intersection without Lemmatizer', keyword_set)
    ST = len(keyword_set)

    keyword_lemma_set = set.intersection(set(a_keyword_lemma),set(q_keyword_lemma))
    #print('Keyword Intersection with Lemmatizer', keyword_lemma_set)
    NON_ST = len(keyword_lemma_set)

    ST = ST / len(q_keyword)
    NON_ST = NON_ST / len(q_keyword_lemma)

    #print('\nKeyword overlap without Lemma = ', ST*100,'%')
    #print('Keyword overlap with Lemma = ', NON_ST*100,'%')
    #print('\n')
    return ST, NON_ST

def n_grams(question, answer, N=4):

    question = question.replace('.','')
    answer = answer.replace('.','')

    question_words = question.lower().split()
    answer_words = answer.lower().split()

    q_grams = nltk.ngrams(question_words, N)
    a_grams = nltk.ngrams(answer_words, N)

    q_list = []
    a_list = []

    for gram in q_grams:
        q_list.append(gram)

    for gram in a_grams:
        a_list.append(gram)

    #print(q_list)
    #print('\n')
    #print(a_list)

    common_grams = set.intersection(set(q_list),set(a_list))
    #print('\nCommon phrases = ',common_grams)

    return len(common_grams)

if __name__=='__main__':

    question =  'The first law of motion was written by Newton.'
    answer =    'Newton wrote the first law of motion.'

    print('\nQuestion = ',question)
    print('\nAnswer = ',answer)
    print('\n')

    #get_multiplier(question, answer)
    n_grams(question, answer)
