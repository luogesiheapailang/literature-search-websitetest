import re
from gensim import corpora, models, similarities
import nltk


def conclude_topic(data, model = 'LSI'):
    if data['AB'] == '' or data['TI'] == '':
        return False
    d1 = ' '.join([i[0].lower() + i[1:] for i in data['AB'].split('. ')]) # 去掉概要首字母大写
    documents = [data['TI'][0].lower() + data['TI'][1:], d1] # 去掉标题首字母大写
    documents = [''.join(re.sub(r'[()\[\],]', '', doc)) for doc in documents]  # 提取出单词，删除了所有括号
    documents[1] += documents[0] # 概要后面加上标题

    # 引入停用词表
    stoplist = ['e.g.']
    # 从作者中增加停用词
    stoplist += data['AU'].split(', ')

    # 只分析长度>2且不在停用词表中的词
    texts = []
    for document in documents:
        words = []
        for word in document.split():
            if len(word) > 2 and word not in stoplist and '/' not in word:
                words.append(word)
        texts.append(words)
    # print(texts)

    '''
    # 去掉简介中只出现一次的单词
    frequency = {}
    for word in texts[1]:
        frequency[word]= frequency.get(word, 0) + 1
    for k,v in frequency.items():
        if v > 1:
            break
    else:
        return False
    texts = [[word for word in text if frequency[word] > 1] for text in texts]
    print(sorted(frequency.items(), key=lambda x:x[1], reverse=True)) # 按频率降序打印出现的词
    '''

    # 标注单词词性
    for i in range(len(texts)):
        tagged_words = nltk.pos_tag(texts[i])
        # 筛选出名词
        texts[i] = [word for word, tag in tagged_words if tag.startswith('N')]
    # print(texts)

    # 生成词典
    dictionary = corpora.Dictionary(texts)  # 进行词典构造时，texts必须是2维的array，即两个中括号[[]]
    # print(dictionary.token2id) # 查看每个词汇对应的id

    # 将整个原始语料库转换为向量列表
    bow_corpus = [dictionary.doc2bow(text) for text in texts]
    # print(bow_corpus) # bow_corpus是经过向量表示的

    # 构建（词频-逆文档频率）模型
    tfidf = models.TfidfModel(bow_corpus)
    # 将整个语料库转为tf-idf格式
    corpus_tfidf = tfidf[bow_corpus]

    if model == 'LSI':
        # 使用主题模型-LSI模型
        topic_model = models.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=2)
        # corpus_lsi = topic_model[corpus]
        # print('corpus_lsi：', list(corpus_lsi))

        # 保存模型及导入模型
        # topic_model.save('./model.lsi')
        # topic_model = models.LsiModel.load('./model.lsi')
    else:
        # 主题模型-LDA模型
        topic_model = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=2)
        # corpus_lda = topic_model[corpus_tfidf]
        # print('corpus_lda：', list(corpus_lda))

    # print(topic_model.print_topics())

    dict1 = {}
    if len(topic_model.show_topics()) > 1:
        ls = topic_model.show_topics()[1][1].split(' + ')
        for e in ls:
            l = e[3:].split('*')
            dict1[eval(l[1])] = eval(l[0])

    dict2 = {}
    ls = topic_model.show_topics()[0][1].split(' + ')
    for e in ls:
        l = e[3:].split('*')
        dict2[eval(l[1])] = eval(l[0])

    # print(dict1)
    res = {key: dict1.get(key, 0) + dict2.get(key, 0) for key in set(dict1) | set(dict2)}
    print(res)
    return res



if __name__ == '__main__':
    # 给出一篇文章的title和摘要数据
    data = {
        'TI': 'Sensing an intense phytoplankton bloom in the western Taiwan Strait from radiometric measurements on a UAV',
        'AB': 'Rapid assessment of algal blooms in bays and estuaries has been difficult due to lack of timely shipboard measurements and lack of spatial resolution from current ocean color satellites. Airborne measurements may fill the gap, yet they are often hindered by the high cost and difficulty in deployment. Here we demonstrate the capacity of a low-cost, low-altitude unmanned aerial vehicle (UAV) in assessing an intense phytoplankton (Phaeocystis globosa) bloom (chlorophyll concentrations ranged from 73 to 45.6 mg/m(3)) in Weitou Bay in the western Taiwan Strait. The UAV was equipped with a hyperspectral sensor to measure the water color with a footprint of 5 mat every 30 m distance along the flight track. A novel approach was developed to obtain remote sensing reflectance (R-rs) from the UAV at-sensor radiometric measurements. Compared with concurrent and co-located field measured R-rs (14 stations in total), the UAV-derived R-rs showed reasonable agreement with root mean square difference ranging 0.0028-0.0043 sr(-1) (relative difference similar to 20-32%) of such turbid waters for the six MODIS bands (412-667 nm). The magnitude of the bloom was further evaluated from the UAV-derived R-rs. For the bloom waters, the estimated surface chlorophyll a concentration (Chl) ranged 6-98 mg/m(3), which is 3-50 times of the Chl under normal conditions. This effort demonstrates for the first time a successful retrieval of both water color (i.e., R-rs) and Chl in a nearshore environment from UAV hyperspectral measurements, which advocates the use of UAVs for rapid assessment of water quality, especially for nearshore or difficult-to-reach waters, due to its flexibility, low cost, high spatial resolution, and sound accuracy. (C) 2017 Published by Elsevier Inc.(',
        'AU':'author1,author2',}

    conclude_topic(data, model='LDA')