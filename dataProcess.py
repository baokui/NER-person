#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
import random
def pro_boson_data(path_data):
    def getdict(str0s):
        words = []
        for str0 in str0s:
            p = 0
            while p<len(str0):
                idx = str0[p:].find('{{')
                if idx==-1:
                    break
                idx0 = p+idx+2
                idx1 = idx0+str0[idx0:].find('}}')
                entity = str0[idx0:idx1]
                a = entity.split(': ')
                if len(a)==1:
                    a = entity.split(':')
                entity = a
                tag = entity[0]
                word = entity[1]
                words.append(word)
                p = idx1+2
        return words
    def parser(str0):
        #jieba.load_userdict("data_zh/dict.txt")
        words = []
        tags = []
        p = 0
        while p<len(str0):
            idx = str0[p:].find('{{')
            if idx!=0 and idx!=-1:
                words.extend(list(str0[p:p+idx]))
                tags.extend(['O']*idx)
                p = p+idx
                continue
            if idx==-1:
                words.extend(list(str0[p:]))
                tags.extend(['O']*len(str0[p:]))
                break
            idx0 = p+idx+2
            idx1 = idx0+str0[idx0:].find('}}')
            entity = str0[idx0:idx1]
            a = entity.split(': ')
            if len(a)==1:
                a = entity.split(':')
            entity = a
            tag = entity[0]
            word = entity[1]
            if tag=='person_name':
                words.extend(list(word))
                tags.append('B-PER')
                for i in range(1,len(word)):
                    tags.append('I-PER')
            else:
                words.extend(list(word))
                tags.extend(['O']*len(word))
            p = idx1+2
        T = [words[i]+' '+tags[i] for i in range(len(words))]
        T += ['. O\n']
        T = '\n'.join(T)
        return T
    def parser_words(path):
        jieba.load_userdict("data_zh/dict.txt")
        #path = 'data_zh/boson.txt'
        with open(path,'r',encoding='utf-8') as f:
            s = f.read().strip().split('\n')[2:]
        T = []
        i = 0
        t = []
        while i < len(s):
            if s[i]=='':
                T.append(t)
                i+=1
                t = [s[i]]
            else:
                t.extend([s[i]])
                i+=1
        T.append(t)
        S = []
        for t in T:
            a = [tt.split(' ') for tt in t]
            chars = [a[i][0] for i in range(len(a))]
            tags = [a[i][-1] for i in range(len(a))]
            for ii in range(len(chars)):
                if len(chars[ii])==0:
                    chars[ii] = ' '
            s = ''.join(chars)
            s = list(jieba.cut(s))
            Tags = []
            M = 0
            last_tag = 'O'
            for i in range(len(s)):
                if tags[M]=='O':
                    Tags.append('O')
                    M += len(s[i])
                    last_tag = 'O'
                    continue
                if last_tag=='O':
                    Tags.append('PER-B')
                    last_tag = 'PER-B'
                else:
                    Tags.append('PER-I')
                    last_tag = 'PER-I'
                M += len(s[i])
            D = [s[i] + '\t' + Tags[i] for i in range(len(s))]
            D = '\n'.join(D)+'\n'
            S.append(D)
        S = ['-DOCSTART-\tO\n'] + S
        with open('data_zh/boson_words.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(S))
    path_data = 'D:\\项目\\NLP-Corpus\\NER\\ChineseNER-data\\boson\\origindata.txt'
    with open(path_data,'r',encoding='utf-8') as f:
        s = f.read().strip()
    s = s.split('\n')
    words = getdict(s)
    with open('data_zh/dict.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(words))
    T = [parser(str0) for str0 in s]
    T = ['-DOCSTART- O\n']+T
    with open('data_zh/boson.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(T))
    parser_words(path='data_zh/boson.txt')
def pro_MSRA_data(path_data):
    # path_data = 'D:\\项目\\NLP-Corpus\\NER\\ChineseNER-data\\MSRA\\train1.txt'
    # path_data = 'D:\\项目\\NLP-Corpus\\NER\\ChineseNER-data\\MSRA\\test1.txt'
    with open(path_data, 'r', encoding='utf-8') as f:
        s = f.read().strip()
    S = s.split('\n')
    f = open('data_zh/MSRA_test_words.txt','w',encoding='utf-8')
    f.write('-DOCSTART-\tO\n\n')
    Words = []
    for s in S:
        t = s.split(' ')
        t = [tt.split('/') for tt in t if len(tt.split('/'))==2]
        words = [tt[0] for tt in t]
        Words.extend(words)
        tags = [tt[1] for tt in t]
        for ii in range(len(tags)):
            if tags[ii]!='nr':
                tags[ii]='O'
            else:
                tags[ii]='PER-B'
        st = [words[i]+'\t'+tags[i] for i in range(len(tags))]
        f.write('\n'.join(st)+'\n\n')
    Words = list(set(Words))
    with open('data_zh/dict.txt','r',encoding='utf-8') as f:
        D = f.read().strip().split('\n')
    Words.extend(D)
    Words = list(set(Words))
    with open('data_zh/dict.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(Words))
def pro_renmin_data():
    path_data = 'D:\\项目\\NLP-Corpus\\NER\\ChineseNER-data\\renMinRiBao\\renmin.txt'
    with open(path_data,'r',encoding='utf-8') as f:
        S = f.read().split('\n\n')
    f = open('data_zh/renmin_words.txt', 'w', encoding='utf-8')
    f.write('-DOCSTART-\tO\n\n')
    Words = []
    for s in S:
        a = s.split('\n')
        a = [' '.join(aa.split('  ')[1:-1]) for aa in a]
        b = ' '.join(a)
        t = b.split(' ')
        t = [tt.split('/') for tt in t if len(tt.split('/')) == 2]
        words = [tt[0] for tt in t]
        Words.extend(words)
        tags = [tt[1] for tt in t]
        lasttag = 'O'
        for ii in range(len(tags)):
            if tags[ii] != 'nr':
                tags[ii] = 'O'
                lasttag = 'O'
            else:
                if lasttag=='PER-B':
                    tags[ii] = 'PER-I'
                    lasttag = 'PER-I'
                else:
                    tags[ii] = 'PER-B'
                    lasttag = 'PER-B'
        st = [words[i] + '\t' + tags[i] for i in range(len(tags))]
        f.write('\n'.join(st) + '\n\n')
    Words = list(set(Words))
    with open('data_zh/dict.txt', 'r', encoding='utf-8') as f:
        D = f.read().strip().split('\n')
    Words.extend(D)
    Words = list(set(Words))
    with open('data_zh/dict.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(Words))
def pro_merge_all():
    files = ['data_zh/boson_words.txt','data_zh/MSRA_train_words.txt','data_zh/MSRA_test_words.txt','data_zh/renmin_words.txt']
    S = []
    for file in files:
        with open(file,'r',encoding='utf-8') as f:
            T = f.read().strip().split('\n\n')[1:]
        S = S+T
    random.shuffle(S)
    r0 = int(0.8*len(S))
    r1 = int(0.9*len(S))
    Train = ['-DOCSTART-\tO'] + S[:r0]
    Test = ['-DOCSTART-\tO'] + S[r0:r1]
    Dev = ['-DOCSTART-\tO'] + S[r1:]
    with open('data_zh/train.txt','w',encoding='utf-8') as f:
        f.write('\n\n'.join(Train))
    with open('data_zh/test.txt','w',encoding='utf-8') as f:
        f.write('\n\n'.join(Test))
    with open('data_zh/dev.txt','w',encoding='utf-8') as f:
        f.write('\n\n'.join(Dev))