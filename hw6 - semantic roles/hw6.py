import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier


def get_all_predicates():
    file_data = pd.read_table('pb-argdefs.tsv')
    return list(set(file_data['base']))


def proceed_conll_file(path):
    file_content = open(path, encoding='utf-8')
    sentences = []
    line = file_content.readline()
    while line:
        if line != '':
            sentences.append(line)
        line = file_content.readline()
    return sentences

def encode_categorical_data(sent_list):
    words, pos1, pos2, sm, role = [], [], [], [], []
    for sent in sent_list:
        if(not sent.startswith('# doc-name:') or not sent.startswith('# sentence-text')):
            s_parts = sent.split('\t')
            words.append(s_parts[2])
            pos1.append(s_parts[3])
            pos2.append(s_parts[4])
            sm.append(s_parts[7])
            rs = sent(s_parts[8].split('|'))
            for r in rs:
                if(len(r.split(':')) > 1):
                    role.append(r.split(':')[1])
                else:
                    role.append(r.split(':')[0])
    return words, pos1, pos2, sm, role


def extracting_arguments(sent_list):
    features, answers, dependencies = [], [], []
    predicates = []
    for sent in sent_list:
        if (not sent.startswith('# doc-name:') or not sent.startswith('# sentence-text')):
            s_parts = sent.split('\t')
            word = s_parts[2]
            pos1 =  s_parts[3]
            pos2 = s_parts[4]
            dep = s_parts[6]
            sm = s_parts[7]
            pred = (word in all_predicates)
            root = (sm == 'root' and int(dep) == 0)
            dependencies.append(dep)
            features.append((label_encoders[0].transform([word])[0], label_encoders[1].transform([pos1])[0],
                             label_encoders[2].transform([pos2])[0], label_encoders[3].transform([sm])[0], pred, root))
            if s_parts[8] == "_":
                answers.append(0)
            else:
                answers.append(1)
    return features, answers, dependencies

def get_argument_types(sent_list):
    features, answers = [], []
    for sent in sent_list:
        s_parts = sent.split('\t')
        word = s_parts[2]
        pos1 = s_parts[3]
        pos2 = s_parts[4]
        sm = s_parts[7]
        features.append((label_encoders[0].transform([word])[0], label_encoders[1].transform([pos1])[0],
                         label_encoders[2].transform([pos2])[0], label_encoders[3].transform([sm])[0]))
        spl = s_parts[8].split('|')[0]
        if spl.split(':')[1]:
            x = spl.split(':')[1]
        else:
            x = spl.split(':')[0]
        answers.append(label_encoders[4].transform([x])[0])
    return features, answers






all_predicates = get_all_predicates()
label_encoders = []
for i in range(5):
    label_encoders.append(preprocessing.LabelEncoder())
sentences_train = proceed_conll_file('fipb-ud-train.conllu')
sentenses_test = proceed_conll_file('fipb-ud-test.conllu')
all_words, all_pos1, all_pos2, all_sm, all_role = encode_categorical_data(sentences_train + sentenses_test)
label_encoders[0].fit(all_words)
label_encoders[1].fit(all_pos1)
label_encoders[2].fit(all_pos2)
label_encoders[3].fit(all_sm)
label_encoders[4].fit(all_role)

train_features, train_answers, train_deps = extracting_arguments(sentences_train)
test_features, test_answers, test_deps = extracting_arguments(sentenses_test)

classifier = DecisionTreeClassifier()
classifier.fit(train_features, train_answers)

preds = classifier.predict(test_features)

feat_arg_train, answ_arg_train = get_argument_types(sentences_train)
feat_arg_test, answ_arg_test = get_argument_types(sentenses_test)
clf = DecisionTreeClassifier()
clf.fit(feat_arg_train, answ_arg_train)

predicted_types = clf.predict(feat_arg_test)
print(classification_report(answ_arg_test, predicted_types))




