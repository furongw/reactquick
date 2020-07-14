from urllib import request
import os
import argparse
import pandas as pd
from pydub import AudioSegment
import random
from tqdm import tqdm
import numpy as np


class reactionquick():
    def __init__(self, args):
        self._type = args.type
        self._split = args.split
        self._from = args.frompath
        self._to = args.topath
        self._number = args.number
        self._store = args.store
        self.interval = args.interval
        if not os.path.exists(self._from):
            raise Exception('there are no word lists')
        if not os.path.exists(self._to):
            os.makedirs(self._to)

        if not os.path.exists(self._store):
            os.makedirs(self._store)

    def get_words(self):
        # 判断是否是文件夹或文件
        if self._split != 'list':
            if os.path.isdir(self._from):
                wordlist = []
                for filename in tqdm(os.listdir(self._from), desc='geting words'):
                    path = os.path.join(self._from, filename)
                    wl = self.get_words_in_file(path)
                    wordlist.extend(wl)
            else:
                wordlist = self.get_words_in_file(self._from)
            return wordlist
        else:
            filename, filetype = os.path.splitext(self._from)
            if not filetype in ['.csv', '.xlsx', '.xls'] or os.path.isdir(self._from):
                raise TypeError('cannot read this kind of file')
            worddict = self.get_words_in_file(self._from)
            return worddict

    def get_words_in_file(self, path):
        filename, filetype = os.path.splitext(path)
        if filetype in ['.csv', '.xlsx', '.xls']:
            if filetype == 'csv':
                data = pd.read_csv(path, header=None)
            else:
                data = pd.read_excel(path, header=None)
        else:
            raise Exception('not readable files')
        if self._split != 'list':
            return data.iloc[:, 0].to_list()
        else:
            datadict = {}
            for words in data.iloc[:, 0].to_list():
                if words.startswith('list'):
                    listnum = words
                    datadict[words] = []
                else:
                    datadict[listnum].append(words)
        return datadict

    def combine_mp3(self, wordlist):
        # 词组内和词组间的间隔
        blank = AudioSegment.from_mp3('blank.mp3')
        interval = blank[:self.interval * 1000]
        all = blank[:  1000]
        for words in wordlist:
            words = words.lower()
            filename = words + '.mp3'
            add = AudioSegment.from_mp3(os.path.join(self._store, filename))
            db1 = -21
            db2 = add.dBFS
            dbplus = db1 - db2
            if dbplus < 0:
                add -= abs(dbplus)
            else:
                add += abs(dbplus)
            # 词组间间隔3s
            all += (add+ interval)
        return all

    def get_word_mp3(self, word):
        """
        get mp3 of the word and download into store
        :param (str) word: lower word or words
        :return:
        """
        word = word.lower()
        filename = word + '.mp3'
        filepath = os.path.join(self._store, filename)
        if not os.path.exists(filepath):
            # 文件不存在，下载
            if self._type == 'E':
                voicetype = '1'
            elif self._type == 'A':
                voicetype = '0'
            length = len(word.split(' '))
            if length >1:
                word = word.replace(' ', '%20')
            url = r'http://dict.youdao.com/dictvoice?type=' + voicetype + r'&audio=' + word
            request.urlretrieve(url, filename=filepath)

    def generate_from_list(self):
        """
        top level
        order: get words -> download words -> split and combine mp3
        :return:
        """
        print('please make sure you put words in first column and no header')
        wordlist = self.get_words()

        if self._split == 'random':
            random.shuffle(wordlist)

        # download mp3s
        if self._split != 'list':
            for words in tqdm(wordlist, desc='downloading sources'):
                words = words.strip().split(' ')
                self.get_word_mp3(words)
        else:
            for listnum, wordslist in tqdm(wordlist.items(), desc='downloading from list'):
                for words in tqdm(wordslist,desc='downloading sources'):
                    words = words.lower()
                    self.get_word_mp3(words)

        # split and combine mp3
        # split wordlist in number
        if self._split != 'list':
            count = 0
            for start in tqdm(range(0, len(wordlist), self._number), desc='combining lists'):
                count += 1
                end = min(start + self._number, len(wordlist))
                sound = self.combine_mp3(wordlist[start:end])
                sound.export(os.path.join(self._to, 'list{}.mp3'.format(str(count))), format='mp3')
        else:
            for listnum, words in tqdm(wordlist.items(), desc='combining lists'):
                sound = self.combine_mp3(words)
                sound.export(os.path.join(self._to, '{}.mp3'.format(str(listnum))), format='mp3')

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--type', choices=['E', 'A'], default='E', help='English accent or American accent')
    argparser.add_argument('--split', choices=['random', 'order', 'list'], default='list',
                           help='how to split the word lists and generate dictate lists')
    argparser.add_argument('--number', default=50, type=int, help='how many words dictated at onetime')
    argparser.add_argument('--frompath', default='example.xlsx')
    argparser.add_argument('--topath', default='dictate')
    argparser.add_argument('--store', default='store', help='where to store all the mp3')
    argparser.add_argument('--interval', default=1, type=float, help='interval among words')
    args = argparser.parse_args()
    a = reactionquick(args)
    a.generate_from_list()
