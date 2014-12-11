__author__ = 'ogaki'
import pickle
import sys
import os
sys.path.append(os.path.dirname(__file__)+"/..")
import nicovideo_comment_distance

DIR = os.path.dirname(__file__)+"/../static"
COMMENT_LIMIT = 30000


if __name__ == '__main__':
    nicovideo = nicovideo_comment_distance.service.Nicovideo()

    with open(sys.argv[1]) as f:
        smids = [line.rstrip() for line in f]

    for id in smids:
        print id
        nicovideo.getvideoinfo(id).comments()
        comments = [comment for comment in nicovideo.getvideoinfo(id).comments(COMMENT_LIMIT)]
        with open(DIR+"/{}".format(id), "w+") as f:
             pickle.dump(comments, f)

    # with open(FILE) as f:
    #     comments = pickle.load(f)
    #
    # import collections
    #
    # comment_dict = collections.defaultdict(int)
    # for comment in comments:
    #     comment_dict[comment.text] += 1
    #
    # for k, v in sorted(comment_dict.items(), key=lambda x: -x[1])[:50]:
    #     print k, v