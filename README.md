とにかく自分の分析を作る
--------------------

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

※ただしHerokuは海外にあるため、公式動画など一部の動画はコメントが取得できません。日本国内に自分のサーバーを建ててdockerの方を動かせば使えます。

↓デプロイページのイメージ

<img width="50%" src="https://raw.githubusercontent.com/Hi-king/niconico_comment_distance/master/README/deploy.png" >

環境変数
--------------
|変数名|意味|
|----|----|
|MAIL|ニコニコのメールアドレス|
|PASS|ニコニコのパスワード|
|VIDEO_ID|難民を探したいVIDEOのID(smXXXX)|
|DESCRIPTION|説明(アプリ中で使われます。５文字前後が良い)|


できること
---------------

ごちうさ分析例: <http://hi-king.hatenablog.com/entry/2014/12/13/091527>


陰陽師分析例

<img width="50%" src="https://raw.githubusercontent.com/Hi-king/niconico_comment_distance/master/README/onmyoji.png" >


Dockerで試す
---------------

```
docker build -t niconico_comment_distance .
docker run -p 80:5000 -e MAIL=your@mail -e PASS=your_pass -e VIDEO_ID=sm9 -e DESCRIPTION="ONMYOJI" --rm -t niconico_comment_distance
curl localhost
```
