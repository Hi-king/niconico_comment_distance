__author__ = 'ogaki'
import sys
import os
sys.path.append(os.path.dirname(__file__)+"/..")
import nicovideo_comment_distance

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        smids = filter(lambda x: len(x)>0, [line.rstrip() for line in f])
    pyon_service = nicovideo_comment_distance.statistic.DistanceFromPyon("1397552685", smids)

    for id in smids:
        distance = pyon_service.distance(id)
        print distance.meta2.title.encode("utf-8"), distance.distance
