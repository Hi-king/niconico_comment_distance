# -*- coding: utf-8 -*-
__author__ = 'ogaki'
import pickle
import collections
import sys
import os
import sklearn
import sklearn.decomposition
import scipy
from placeholder import ___
sys.path.append(os.path.dirname(__file__)+"/..")
import nicovideo_comment_distance

DIR = os.path.dirname(__file__)+"/../static"
TOP_WORDS_NUM = 10000000000000 #topn words to get word dict
TOP_WORDS_NUM = 10 #topn words to get word dict
TOP_WORDS_NUM = 10000000000000 #topn words to get word dict

if __name__ == '__main__':
    nicovideo = nicovideo_comment_distance.service.Nicovideo()

    with open(sys.argv[1]) as f:
        smids = filter(lambda x: len(x)>0, [line.rstrip() for line in f])

    # video_meta_dict = {k: nicovideo.getvideometa(k) for k in smids}
    # with open(DIR+"/metas.pickle", "w+") as f:
    #     pickle.dump(video_meta_dict, f)
    with open(DIR+"/metas.pickle") as f:
        video_meta_dict = pickle.load(f)


    words = set()

    # get words
    for id in smids:
        print id
        with open(DIR+"/{}".format(id)) as f:
             comments = pickle.load(f)
        comment_dict = collections.defaultdict(int)
        for comment in comments:
            if comment.text is None or len(comment.text) == 0: continue
            comment_dict[comment.text] += 1
        for k, v in sorted(comment_dict.items(), key=lambda x: -x[1])[:TOP_WORDS_NUM]:
            words.add(k)
            # print k, v

    # word vec
    video_matrix = []
    for id in smids:
        print id
        with open(DIR+"/{}".format(id)) as f:
             comments = pickle.load(f)
        word_dict = {k: 0 for k in words}
        for comment in comments:
            if comment.text in words:
                word_dict[comment.text] += 1

        # for k,v in word_dict.items():
        #     vector.ap
        #     video_matrix[k].append(v)
        video_matrix.append([word_dict[word] for word in words])

    mat = scipy.array(video_matrix, scipy.float32)

    # for word, vec in zip(words, mat.T):
    #     print word, vec


    # for k,v in video_matrix.items():
    #     print k
    #     print v

    #tf
    tf = 0.5+0.5*mat/(mat.max(axis=1).reshape(mat.shape[0],1))

    #idf
    idf = scipy.ones((mat.shape[0], 1)) * (scipy.log(float(mat.shape[0])/((mat != 0).sum(axis=0))))

    tfidf = tf * idf
    print tfidf

    # pca = sklearn.decomposition.PCA(n_components=2)
    #
    # coordinates = {}
    # for id, [x,y] in zip(smids, pca.fit_transform(tf)):
    #     coordinates[id] = [x, y]
    #     print id,x,y
    # for id, [x,y] in coordinates.items():
    #     tx, ty = coordinates["1397552685"]
    #     print id, scipy.sqrt((tx-x)**2 + (ty-y)**2)



    raw_vecs = {id: vec for id, vec in zip(smids, mat)}
    shows = []
    ## euclid
    # for id, vec in raw_vecs.items():
    #     dims = [[w, abs(x-tx), [x,tx]] for w,x,tx in zip(words, vec, raw_vecs["1397552685"])]
    #     dims.sort(key=lambda x: -x[1])
    #     shows.append([id, scipy.linalg.norm(vec - raw_vecs["1397552685"]), video_meta_dict[id].title, dims[:5]])

    ## cosine
    for id, vec in raw_vecs.items():
        tvec = raw_vecs["1397552685"]
        vnorm = scipy.linalg.norm(vec)
        tvnorm = scipy.linalg.norm(tvec)
        dims = [[w, x*tx/vnorm/tvnorm, [x, tx]] for w, x, tx in zip(words, vec, tvec)]
        dims.sort(key=lambda x: -x[1])
        shows.append([id, sum([dim[1] for dim in dims]), video_meta_dict[id].title, dims[:5]])
    for id, dist, title, dims in sorted(shows, key=___[1]):
        print id, dist, title.encode("utf-8")
        for k, val, [x, tx] in dims:
            print k.encode("utf-8"), val, [x, tx]
