import os
import nltk
from nltk.corpus import stopwords
from textblob import Word
from textblob import TextBlob
import re
import math
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC, SVC



def get_all_files(text_folder):
    text_files = []
    key_files = []
    for file in os.listdir(text_folder):
        if file.endswith('.txt'):
            text_files.append(file)
        elif file.endswith('.key'):
            key_files.append(file)
    return text_files, key_files


def get_all_texts(text_files, texts_folder):
    all_texts = []
    for file in text_files:
        f = open(texts_folder + file, 'r', encoding='utf-8')
        all_texts.append(f.read())
    return all_texts


def get_keywords_from_file(path):
   return open(path).read().split('\n')


def get_all_features(texts):
    i = 41
    all_features = []
    all_answers = []
    for text in texts:
        text_l = text.value.lower()
        words = TextBlob(text_l).words
        lemmas = []
        for word in words:
            w = Word(word)
            lemma = w.lemmatize()
            lemmas.append(lemma)
            pos = get_part_of_speech_data(lemmas)
            pkw = get_possible_key_words(pos, lemmas)
            p = 'C-' + str(i)
            keys_f = get_keywords_from_file(p)
            for kw in pkw:
                features, answers = [], []
                tf = get_tf(kw, lemmas)
                features.append(tf)
                idf = get_idf(tf, word, texts)
                features.append(idf)
                all_features.append(features)

                if kw in keys_f:
                    answers.append('1')
                else:
                    answers.append('0')
                all_answers.append(answers)
            i = i + 1
    return all_features, all_answers



def get_tf(word, lemmas):
    return len(re.findall(word, ' '.join(lemmas)))/float(len(lemmas))

def get_idf(tf, word, texts):
    df = 0
    for text in texts:
        if word in texts:
            df += 1
    return tf*math.log(df/float(len(texts)))


def get_part_of_speech_data(lemmas):
    result = []
    for lemma in lemmas:
        result.append(nltk.pos_tag(lemma))
    return result


def get_possible_key_words(part_of_speech_data, lemmas):
    pkws = []
    for i in range(len(part_of_speech_data) - 1):
        if (part_of_speech_data[i][1] == 'NN' or part_of_speech_data[i][1] == 'JJ') and (
                    part_of_speech_data[i + 1][1] == 'NN') and len(
            part_of_speech_data[i][1]) > 1 and len(part_of_speech_data[i + 1][1]) > 1:
            t = part_of_speech_data[i][0] + u' ' + part_of_speech_data[i + 1][0]
            if t not in pkws and '|' not in t and len(re.findall(t, ' '.join(lemmas))) > 1:
                pkws.append(t)
    for i in range(len(part_of_speech_data) - 2):
        if (part_of_speech_data[i][1] == 'NN' or part_of_speech_data[i][1] == 'JJ') and (
                    part_of_speech_data[i + 1][1] == 'NN') and (
                    part_of_speech_data[i + 2][1] == 'NN') and len(part_of_speech_data[i][1]) > 1 and len(
            part_of_speech_data[i + 1][1]) > 1 and len(
            part_of_speech_data[i + 2][1]) > 1:
            t = part_of_speech_data[i][0] + u' ' + part_of_speech_data[i + 1][0] + u' ' + part_of_speech_data[i + 2][0]
            if t not in pkws and '|' not in t and len(re.findall(t, ' '.join(part_of_speech_data))) > 1:
                pkws.append(t)

    return  pkws




train_text_files, train_key_files = get_all_files('maui-semeval2010-train\\')
train_texts = get_all_texts(train_text_files, 'maui-semeval2010-train\\')
train_features, train_answers = get_all_features(train_texts)
test_text_files, test_key_files = get_all_files('maui-semeval2010-test\\')
test_texts = get_all_texts(test_text_files, 'maui-semeval2010-test\\')
test_features, test_answers = get_all_features(test_texts)

model = svm.LinearSVC(class_weight = 'balanced', random_state = 42)
model.fit(train_features, train_answers)
predictions = model.predict(test_features)
print(classification_report(test_answers, predictions))


