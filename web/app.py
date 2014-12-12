__author__ = 'ogaki'
from flask import Flask, jsonify, render_template
import sys
import os
import re
sys.path.append(os.path.dirname(__file__)+"/..")
import nicovideo_comment_distance


with open(sys.argv[1]) as f:
    smids = filter(lambda x: len(x)>0, [line.rstrip() for line in f])
pyon_service = nicovideo_comment_distance.statistic.DistanceFromPyon("1397552685", smids)

app = Flask(__name__)


video_id_queue = [None for i in xrange(30)]

@app.route("/")
def top():
    return render_template("top.html", video_id_queue=video_id_queue)

@app.route("/distance/<video_id>")
def distance(video_id):
    # validation
    p = re.compile('[sm0-9]*')
    if not p.match(video_id):
        return None

    # calc distance
    distance = pyon_service.distance(video_id)
    if not video_id in video_id_queue:
        video_id_queue.append(video_id)
        video_id_queue.pop(0)
    return jsonify({
        "title": distance.meta2.title,
        "distance": distance.distance
    })


if __name__ == "__main__":
    app.run(debug=True)