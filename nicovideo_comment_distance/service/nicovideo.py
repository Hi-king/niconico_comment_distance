# -*- coding: utf-8 -*-
__author__ = 'ogaki'

import urllib2
from BeautifulSoup import BeautifulSoup
import mechanize
import re
import htmlentitydefs
import time
import unicodedata
import itertools
import os

###########
## const ##
###########

class Config:
    MAIL = os.environ.get("MAIL")
    PASS = os.environ.get("PASS")

Browser = mechanize.Browser()
Browser.set_handle_robots(False)

class Comment:
    def __init__(self, text, date):
        self.text = self.normalize(text)
        self.date = date

    # def str_ignore_invalid_char(self, text):
    #     """
    #     参考: http://d.hatena.ne.jp/torasenriwohashiru/20110806/1312558290
    #     """
    #     if isinstance(text, unicode):
    #         return unicodedata.normalize('NFKC', text)
    #     return text

    def cyclic_normalize(self, text):
        """
        (1,2,3)文字の連続を吸収
        e.g. wwwwww -> w
        """
        lasts = [" ", " ", "  ", "   "]
        i = 0
        ret = ""
        while i < len(text):
            ret += text[i]
            for j in xrange(1, len(lasts)):
                lasts[j] = lasts[j][1:]
                lasts[j] += text[i]
            while True:
                if text[i:i+1] == lasts[1]: i+=1
                elif text[i:i+2] == lasts[2]: i+=2
                elif text[i:i+3] == lasts[3]: i+=3
                else: break
        return ret


    def normalize(self, text):
        """
        正規化
        参考: http://d.hatena.ne.jp/torasenriwohashiru/20110806/1312558290
        """
        # 空白除去
        if text is None: return None
        unicode_normalized = unicodedata.normalize('NFKC', text)
        normalized = "".join(unicode_normalized.split())
        cyclic_normalized = self.cyclic_normalize(normalized)
        return cyclic_normalized



class VideoInfo:
    def __init__(self, video_id, thread_id, ms, user_id, **lest_dict):
        # url = "http://flapi.nicovideo.jp/api/getflv/{}".format(video_id)
        self.thread_id = thread_id
        self.ms = ms
        self.user_id = user_id
        threadkeyinfo = self.__getthreadkey()
        self.threadkey = threadkeyinfo["threadkey"]
        self.force_184 = threadkeyinfo["force_184"]
        self.waybackkey = self.__getwaybackkey()["waybackkey"]

    def comments(self, size=10):
        def comments_generator():
            response = self.__fetch_comment()
            for chat in reversed(response.find("packet").findAll("chat")):
                comment = Comment(chat.string, int(chat["date"]))
                yield comment

            while True:
                response = self.__fetch_comment(date=comment.date)
                for chat in reversed(response.find("packet").findAll("chat")):
                    comment = Comment(chat.string, int(chat["date"]))
                    yield comment

        return itertools.islice(comments_generator(), 0, size)
        # for comment in itertools.islice(comments_generator(), 0, size):
        #     print "\t".join([str(comment.date), comment.text.encode("utf-8")])




    def __fetch_comment(self, date=None):
        if date is None: date = int(time.time())
        xml = '''
        <thread
            thread="{0}"
            version="20061206"
            res_from="-1000"
            waybackkey="{1}"
            when="{2}"
            user_id="{3}"
            threadkey="{4}"
            scores="1"
            force_184="{5}"
        />
        '''.format(self.thread_id, self.waybackkey, date, self.user_id, self.threadkey, self.force_184)

        # print xml

        body = Browser.open(self.ms, xml).read()
        return BeautifulSoup(body)


    def __getwaybackkey(self):
        url = "http://flapi.nicovideo.jp/api/getwaybackkey?thread={}".format(self.thread_id)
        return self.__urlquoted2dict(Browser.open(url).read())

    def __getthreadkey(self):
        url = "http://flapi.nicovideo.jp/api/getthreadkey?thread={}".format(self.thread_id)
        return self.__urlquoted2dict(Browser.open(url).read())

    def __urlquoted2dict(self, response_string):
        raw_list = [token.split("=") for token in response_string.split("&")]
        unquoted_dict = dict([[k, urllib2.unquote(v)] for k,v in raw_list])
        return unquoted_dict


class Nicovideo:
    def __init__(self):
        self.browser = Browser
        self.log_in()

    def log_in(self):
        self.browser.open("https://secure.nicovideo.jp/secure/login?site=niconico")
        self.browser.select_form(nr=0)
        self.browser["mail_tel"]=Config.MAIL
        self.browser["password"]=Config.PASS
        self.browser.submit()


    def getvideoinfo(self, video_id):
        flvinfo = self.__getflvinfo(video_id)

        return VideoInfo(video_id, **flvinfo)

    def __getflvinfo(self, video_id):
        url = "http://flapi.nicovideo.jp/api/getflv/{}".format(video_id)
        response_string = self.browser.open(url).readline()
#         response_string = """thread_id=1173108780&l=319&url=http%3A%2F%2Fsmile-pcm42.nicovideo.jp%2Fsmile%3Fv%3D9.0468&ms=http%3A%2F%2Fmsg.nicovideo.jp%2F10%2Fapi%2F&ms_sub=http%3A%
# 2F%2Fsub.msg.nicovideo.jp%2F10%2Fapi%2F&user_id=2033423&is_premium=1&nickname=%E3%81%AF%E3%81%84%E3%81%8F&time=1418055816378&done=true&hms=hiroba.nicovideo.jp&hmsp=2592&hmst=680&hmstk=1418055876.x3K0d2A5bw9djRNY8
# 9wbZDHman0"""
        raw_list = [token.split("=") for token in response_string.split("&")]
        unquoted_dict = dict([[k, urllib2.unquote(v)] for k,v in raw_list])
        print unquoted_dict
        return unquoted_dict


    def comment(self, video_id):
        print "http://msg.nicovideo.jp/{}/api".format(video_id)
        url = urllib2.urlopen("http://msg.nicovideo.jp/{}/api".format(video_id))
        print url.read()

    def __htmlentity2unicode(self, text):
        # 正規表現のコンパイル
        reference_regex = re.compile(r'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
        num16_regex = re.compile(r'#x\d+', re.IGNORECASE)
        num10_regex = re.compile(r'#\d+', re.IGNORECASE)

        result = u''
        i = 0
        while True:
           # 実体参照 or 文字参照を見つける
           match = reference_regex.search(text, i)
           print "text"
           print text
           print "match", match
           if match is None:
               result += text[i:]
               break

           result += text[i:match.start()]
           i = match.end()
           name = match.group(1)


           # 実体参照
           if name in htmlentitydefs.name2codepoint.keys():
               result += unichr(htmlentitydefs.name2codepoint[name])
           # 文字参照
           elif num16_regex.match(name):
               # 16進数
               result += unichr(int(u'0'+name[1:], 16))
           elif num10_regex.match(name):
               # 10進数
               result += unichr(int(name[1:]))
        return result
