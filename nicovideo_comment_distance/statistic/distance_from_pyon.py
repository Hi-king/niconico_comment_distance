# -*- coding: utf-8 -*-
__author__ = 'ogaki'

import nicovideo_comment_distance
import collections
import math

class Distance(object):
    def __init__(self, distance, meta1, meta2):
        self.distance = distance
        self.meta1 = meta1
        self.meta2 = meta2

class DistanceFromPyon(object):
    """
    特定動画動画からの距離を計算する
    """
    COMMENT_SIZE = 30000 #一動画あたり何コメントまで考慮するか
    TOP_WORDS_NUM = 30 #一動画あたり上位何コメントまでを

    def __init__(self, target_video_id, ids_for_train):
        self.nicovideo = nicovideo_comment_distance.service.Nicovideo()
        self.comments = self.nicovideo.getvideoinfo(target_video_id).comments(self.COMMENT_SIZE)
        self.meta = self.nicovideo.getvideometa(target_video_id)
        self.ids_for_train = ids_for_train
        self.words = self.__wordset()
        self.video_id = target_video_id
        self.vector = self.__calc_vector(self.comments)

    def __wordset(self):
        words = set()
        # get words
        for id in self.ids_for_train:
            print id
            comments = self.nicovideo.getvideoinfo(id).comments(self.COMMENT_SIZE)
            comment_dict = collections.defaultdict(int)
            for comment in comments:
                if comment.text is None or len(comment.text) == 0: continue
                comment_dict[comment.text] += 1
            for k, v in sorted(comment_dict.items(), key=lambda x: -x[1])[:self.TOP_WORDS_NUM]:
                words.add(k)
        return words

    def __calc_vector(self, comments):
        vector = {k:0 for k in self.words}
        for comment in comments:
            if comment.text in self.words:
                vector[comment.text] += 1
        norm = math.sqrt(sum([val*val for val in vector.values()]))
        return [float(val)/norm for val in vector.values()]

    def distance(self, video_id):
        """
        target_video_idからのDistanceを返す
        :param video_id: string
        :return: Distance
        """
        comments = self.nicovideo.getvideoinfo(video_id).comments(self.COMMENT_SIZE)
        vector = self.__calc_vector(comments)
        meta = self.nicovideo.getvideometa(video_id)
        distance = sum([thisval*otherval for thisval, otherval in zip(self.vector, vector)])
        return Distance(distance=distance, meta1=self.meta, meta2=meta)







