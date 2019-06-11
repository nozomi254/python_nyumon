import json

# まず開きます
with open('novels.json', 'r', encoding='utf-8') as f:
    novels = json.load(f)
# 与えられたテキスト text に含まれるn-gramのリストを返す
# テキストをn-gramにするやつ
def multiline_ngrams(n, text):
    l = []
    for sentence in text.split('\n'):
        for i in range(0, len(sentence)-n+1):
            l.append(sentence[i:i+n])
    return l

# 引数 novels に入っている小説のうち、author が書いた小説に現れる
# すべてのn-gramのリストを返す関数
# 小説を である とかに区切っていく
def author_ngrams(n, author, novels):
  n_author = []
  for i in novels:
    if i['author'] == author:
        n_author += multiline_ngrams(n, i['text'])
  return n_author
# 各々のn-gramをキーとして、 その出現回数を値（バリュー）とする辞書を返す関数
# である とかが何個出てきたか数える
import collections
def histogram(ngs):
    dic = collections.Counter(ngs)
    return dic

dazai_histogram = histogram(author_ngrams(3, '太宰治', novels))
miyazawa_histogram = histogram(author_ngrams(3, '宮沢賢治', novels))
#print(histogram(author_ngrams(3, '太宰治', novels))['である'])

# n-gram出現回数の分布 hist が与えられたら、 n-gramの確率分布を返す関数
# である が出てくる確率
def probability_distribution(hist):
    list1 = list(hist.values())
    n = sum(hist.values())
    values = list(map(lambda x: x / n, list1))
    keys = list(hist.keys())
    dic = dict(zip(keys, values))
    return dic

# 文章がどれくらい近いか
def Tankard(d1, d2):
    co_list = d1.keys() & d2.keys()
    list1 = []
    for i in co_list:
        list1.append(abs(d1[i]-d2[i]))
    return sum(list1) / len(list1)

print(round(Tankard(probability_distribution(dazai_histogram),probability_distribution(miyazawa_histogram))*10**8) == 855)

# 未知の著者の小説を受け取って、太宰治のか宮沢賢治のか返す
def which_author(n, un, novels):
    un_histogram = histogram(author_ngrams(n, un, novels))
    un_dazai = Tankard(probability_distribution(dazai_histogram), probability_distribution(un_histogram))
    un_miya = Tankard(probability_distribution(miyazawa_histogram), probability_distribution(un_histogram))
    if un_dazai < un_miya:
        return '太宰治'
    else:
        return '宮沢賢治'

print(which_author(3,'UN0',novels) == '太宰治')
print(which_author(3,'UN9',novels) == '宮沢賢治')
