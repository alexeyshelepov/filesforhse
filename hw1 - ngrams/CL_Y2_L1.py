import re
import math

def read_file(file_name):
    try:
        file_content = ''
        with open(file_name, 'r', -1, 'utf-8') as file:
            for line in file:
                file_content += line
        return file_content
    except FileNotFoundError:
        return ""


def extract_words(input_text):
    result_text = input_text.lower()
    words_list = re.findall('\w+', result_text)
    return words_list


def count_frequencies(word_list):
    frequencies_dict = {}
    for word in word_list:
        if word in frequencies_dict:
            frequencies_dict[word] += 1
        else:
            frequencies_dict[word] = 1
    return frequencies_dict


def find_bigramms_sorted(main_list, word):
    result_list = []
    total_words = len(main_list)
    i = 1
    while i < total_words - 2:
        if main_list[i + 1] == word:
            result_list.append(main_list[i] + " " + word)
        if main_list[i] == word:
            result_list.append(word + " " + main_list[i + 1])
        i += 1
    bigram_frequences = count_frequencies(result_list)
    bigam_frequencies_sorted = list(bigram_frequences.items())
    bigam_frequencies_sorted.sort(key=lambda item: item[1], reverse=True)
    return bigam_frequencies_sorted


def count_pmi(c_w1, c_w2, c_b, t_w):
    if c_w2 == 0:
        return 0
    p_b = math.log(c_b / (t_w - 1))
    p_w1 = math.log(c_w1 / t_w)
    p_w2 = math.log((c_w2 / t_w))
    return p_b / (p_w1 * p_w2)


def get_word_from_bigram(bigram, word):
    result = bigram.replace(word, "")
    result = result.strip()
    #print(result + " ")
    return result


def write_info_about_word(word, word_list, frequences_list):
    bigrams = find_bigramms_sorted(word_list, word)
    with open('C:\\t2.txt', 'w') as file:
        file.write('word 1\tword 2\tcount(word 1)\tcount(word 2)\tcount(bigram)\n')
        c_w1 = frequences_list[word]
        tot = len(word_list)
        for i in range(0, 100):
            print(i)
            word_2 = get_word_from_bigram(bigrams[i][0], word)
            c_bigram = bigrams[i][1]
            c_w2 = 0

            if word_2 in frequences_list:
                c_w2 = frequences_list[word_2]
            pmi = round(count_pmi(c_w1, c_w2, c_bigram, tot), 3)
            file.write(word + '\t' + word_2 + '\t' + str(c_w1) + '\t' + str(c_w2) + '\t' + str(c_bigram) + '\t' + str(pmi) + '\n')


content = read_file('C:\\text.txt')
words = extract_words(content)
frequences = count_frequencies(words)
write_info_about_word('google', words, frequences)




#print(type(frequences))

