import gensim
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from keras.models import Sequential
from keras.layers import Dense

training_objects = []
features = []
answers = []


class line_obj:
    first_word = ''
    second_word = ''
    third_word = ''
    mes = 0


def perform_line(line):
    elements = line.split(',')
    obj = line_obj()
    obj.first_word = elements[0]
    obj.second_word = elements[1]
    obj.third_word = elements[2]
    obj.mes = int(elements[3])
    training_objects.append(obj)


def reading_test_data():
    f = open('train.txt')
    line = f.readline()
    while line:
        perform_line(line)
        line = f.readline()
    f.close()


def get_features_answers(vector_model):
    for obj in training_objects:
        try:
            cos_sim_13 = vector_model.wv.similarity(obj.first_word, obj.third_word)
            cos_sim_23 = vector_model.wv.similarity(obj.second_word, obj.third_word)
            cos_sim_12 = vector_model.wv.similarity(obj.first_word, obj.second_word)
            features.append((cos_sim_13, cos_sim_23, cos_sim_12))
            answers.append(obj.mes)
        except KeyError:
            print('error')


def init_learning():
    print('starting getting vector model')
    reading_test_data()
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
    print('ending training vector model')
    print('starting getting data for nn')
    get_features_answers(model)
    print('ending getting data for nn')
    return train_test_split(features, answers, test_size=0.2, random_state=33)


def create_neural_network():
    classifier = Sequential()
    classifier.add(Dense(output_dim=6, init='uniform', activation='relu', input_dim=3))
    classifier.add(Dense(output_dim=6, init='uniform', activation='relu'))
    classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))
    classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    classifier.fit(features_train, answers_train, batch_size=10, nb_epoch=100)
    return classifier


features_train, features_test, answers_train, answers_test = init_learning()
neur_net = create_neural_network()
answers_pred = neur_net.predict(features_test)
answers_pred = (answers_pred > 0.5)
cm = confusion_matrix(answers_test, answers_pred)
print(cm)
p = precision_score(answers_test, answers_pred)
print(p)
r = recall_score(answers_test, answers_pred)
print(r)
f1 = f1_score(answers_test, answers_pred)
print(f1)


