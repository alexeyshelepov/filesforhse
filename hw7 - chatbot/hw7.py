import re, random

data = open('1triple_allSolutions_Astronaut_train_challenge.xml', 'r', encoding='utf-8').read()
triples = list(set([re.split('</mtriple>', x)[0].strip() for x in re.split('<mtriple>', data)[1:]]))

lex_do = {}
lex_do['almaMater'] = ['The alma mater of', 'graduated from', 'recieved a Bachelor of science degree']
lex_do['birthDate'] = ['was born on']
lex_do['birthName'] = ['full name is', 'The bitrh name of']
lex_do['birthPlace'] = ['was born in']
lex_do['dateOfRetirement'] = ['reitred in']
lex_do['occupation'] = ['was a', 'served as', 'performed as']
lex_do['status'] = ['is']
lex_do['timeInSpace'] = ['was in space']
lex_do['was a crew member of'] = ['was a crew member of']
lex_do['was selected by NASA'] = ['was selected by NASA in']
lex_do['deathDate'] = ['died on']
lex_do['nationality'] = ['is from', 'The nationality of', 'was from']
lex_do['title'] = ['was', 'served as']
lex_do['backup pilot'] = ['was a backup pilot of']
lex_do['commander'] = ['was the commander of']
lex_do['operator'] = ['was the operator in']
lex_do['crewMembers'] = ['\'s crew members included']
lex_do['representative'] = ['served as representative', 'represented']
lex_do['alternativeNames'] = ['\'s real name was', 'also called as']
lex_do['was awarded'] = ['was awarded with']
lex_do['awards'] = ['had won']
lex_do['part'] = lex_do['isPartOf'] = ['is a part of', 'is located in']
lex_do['leaderName'] = ['\'s leader is']
lex_do['president'] = ['is president of']

lex_ro = {}
lex_ro['leaderName'] = ['was the leader of']
lex_ro['senator'] = ['One of senatoes of']
lex_ro['representative'] = ['is representative of']
lex_ro['crewMembers'] = ['crew members included']
lex_ro['operator'] = ['operated']
lex_ro['commander'] = ['commanded']

keywords = {}
keywords[('university', 'graduated')] = ['almaMater']
keywords[('born', 'birth')] = ['birthDate']
keywords[('full name', 'real name')] = ['birthName']
keywords[('born in',)] = ['birthPlace']
keywords[('retired',)] = ['dateOfRetirement']
keywords[('occupation', 'served', 'perform', 'job')] = ['occupation']
keywords[('status', )] = ['status']
keywords[('time in space',)] = ['timeInSpace']
keywords[('crew member', )] = ['was a crew member of']
keywords[('was selected by NASA', )] = ['was selected by NASA']
keywords[('died', 'death')] = ['deathDate']
keywords[('nationality', 'from')] = ['nationality']
keywords[('backup pilot',)] = ['backup pilot']
keywords[('commander', )] = ['commander']
keywords[('operator', )] = ['operator']
keywords[('representative', )] = ['representative']
keywords[('alternative name', 'pseudonim', 'real name')] = ['alternativeNames']
keywords[('was awarded',)] = ['was awarded']
keywords[('award', )] = ['awards']
keywords[('part', )] = ['part']
keywords[('leader', )] = ['leaderName']
keywords[('president', )] = ['president']
keywords[('senator', )] = ['senator']


while True:
    question = input("> ").lower()
    if question == 'exit':
        break

    topic = ''
    for key in keywords.keys():
        for el in key:
            if el in question:
                topic = keywords[key]
                break

    if topic == '':
        print('I don\'t know that')
    else:
        wo = "direct"
        if topic not in lex_ro:
            wo = "direct"
        elif topic not in lex_do:
            wo = "reversed"

    predicate = ''
    if wo == "direct":
        predicate = random.choice(lex_do[topic])
    else:
        predicate = random.choice(lex_ro[topic])

    subjects, objects = [], []
    for triple in triples:
        subjects.append(triple.split('|')[0].strip())
        objects.append(triple.split('|')[2].strip())

    answer_subj, answer_obj = '', ''
    for subject in subjects:
        if subject.replace('_', ' ').split('(')[0] in question:
            answer_subj = (subject.replace('_', ' ').split('(')[0])
    for obj in objects:
        if obj.replace('_', ' ').split('(')[0] in question:
            obj = obj.replace('_', ' ').split('(')[0]

    if subject == '' or obj == '':
        print('I don\'t know that')
    else:
        if wo == 'direct':
            if predicate[0].isupper():
                print(predicate + ' ' + subject + ' is ' + obj)
            else:
                print(subject +  ' ' + predicate + ' ' + obj)
        else:
            if predicate[0].isupper():
                print(predicate + ' ' + obj + ' is ' + subject)
            else:
                print(obj +  ' ' + predicate + ' ' + subject)

