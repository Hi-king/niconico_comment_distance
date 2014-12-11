# -*- coding:utf-8 -*-
__author__ = 'ogaki'

import sys
import os
sys.path.append(os.path.dirname(__file__)+"/../..")
import unittest
import nicovideo_comment_distance


class CommentNicovideo(unittest.TestCase):
    def test_normalize(self):
        """正規化のテスト"""
        print "test"

        self.assertEqual(
            nicovideo_comment_distance.service.Comment(u"ABC ｱｲｳｴｵ").text,
            u"ABCアイウエオ")

        self.assertEqual(
            nicovideo_comment_distance.service.Comment(u"wwwwwwwwwwwww").text,
            u"w")

        self.assertEqual(
            nicovideo_comment_distance.service.Comment(u"レロレロレロレロ").text,
            u"レロ")
