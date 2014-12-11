# -*- coding:utf-8 -*-
__author__ = 'ogaki'

import sys
import os
sys.path.append(os.path.dirname(__file__)+"/../..")
import unittest
import nicovideo_comment_distance

# class TestVideoInfo(unittest.TestCase):
#     def test_init(self):
#         """getthumbinfoできる"""
#         nicovideo_comment_distance.service.VideoInfo("sm9")

class TestNicovideo(unittest.TestCase):
    def test_comment(self):
        """コメントを取得できることのテスト"""
        print nicovideo_comment_distance.service.Nicovideo().getvideoinfo("sm9")
