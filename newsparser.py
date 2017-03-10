# в python3 такая строчка обычно не нужна
# но если у вас специфичные настройки компьютера
# может пригодиться
# -*- coding: UTF-8 -*-
# Написать программу, которая будет выводить топ 10 самых часто встречающихся в
# новостях слов длиннее 6 символов для каждого файла.
#
#Не забываем про декомпозицию и организацию кода в функции. В решении домашнего задания вам могут помочь: split(), sort или sorted.
import chardet
import os
import json

# with codecs.open('newsfr.json', encoding="iso8859_5") as news:
# 	print(json.load(news))

def get_six_letter(json_string_entry): # Функция для слов длиннее 6 символов
    russian_letters = ''.join([chr(n) for n in range(1040, 1104)]) + 'Ёё'
    symbols_to_strip = "0123456789 !@#$%^&*()-_+={}[]|\:;'<>?,./\""
    entry = json_string_entry.strip(symbols_to_strip)
    word = ''
    result_words = []
    for index, char in enumerate(entry): #Возвращает генератор, отдающий пары счётчик-элемент для элементов указанной последовательности.
        if char not in russian_letters:
            if len(word) > 6:
                result_words.append(word)
            word = ''
        else:
            word += char
            if index == (len(entry) - 1) and len(word) > 6:
                result_words.append(word)
    return result_words


def count_top_ten(dict):
    top_ten = sorted(dict.items(), key=lambda x: x[1], #cравнение словарей производится по значению ключа "1".
              reverse=True)[0:10]
    return top_ten

def get_new_entry(name, charset):
    with open(name, 'r', encoding=charset) as json_source:
        json_dict = json.load(json_source)
    return json_dict

def parser(parsing_dict):
    news_text_string = str(parsing_dict.values())
    word_dict = {}
    for entry in news_text_string.split():
        words = get_six_letter(entry)
        if words:
            for word in words:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
    return word_dict


def print_results(news_entry, top_ten):
    print('Список из 10 самых часто встречающихся слов в файле "{}"\n'.
          format(news_entry))
    for index, word in enumerate(top_ten):
        print('{0:2}.Слово "{1}", встречается {2} раз\n'.
               format(index+1, word[0], word[1]))


def check_encoding(news_file):
    rawdata = open(news_file, "rb").read()
    result = chardet.detect(rawdata)
    open(news_file).close()
    return result['encoding']



def main():
    home_dir = os.getcwd()  #текущая рабочая директория
    news_files = []
    for file in os.listdir(home_dir):
        whole_file_name = os.path.join(home_dir, file)
        if file.endswith('.json'):
            news_files.append(whole_file_name)
            print("загружен файл:", format(file))
    for news_entry in news_files:
        charset = check_encoding(news_entry)
        parsing_dict = get_new_entry(news_entry, charset)
        word_dict = parser(parsing_dict)
        top_ten = count_top_ten(word_dict)
        print_results(news_entry, top_ten)

main()
