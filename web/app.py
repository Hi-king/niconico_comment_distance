__author__ = 'ogaki'
from flask import Flask, jsonify, render_template, request, Blueprint, redirect, url_for
import sys
import os
import re
import chartkick
sys.path.append(os.path.dirname(__file__)+"/..")
import nicovideo_comment_distance


TARGET_VIDEO_ID = os.environ.get("VIDEO_ID") if not os.environ.get("VIDEO_ID") is None else "1397552685"
VIDEO_DESCRIPTION = os.environ.get("VIDEO_DESCRIPTION") if not os.environ.get("VIDEO_DESCRIPTION") is None else TARGET_VIDEO_ID

filepath = os.path.dirname(__file__)+"/../videos/14spring.dat"
with open(filepath) as f:
    smids = filter(lambda x: len(x)>0, [line.rstrip() for line in f])
pyon_service = nicovideo_comment_distance.statistic.DistanceFromPyon(TARGET_VIDEO_ID, smids)

app = Flask(__name__)
# app.jinja_env.add_extention('chartkick.ext.charts')
# app.jinja_env = jinja2.Environment(extensions=['chartkick.ext.charts'])
# app.jinja_env = jinja2.Environment(extensions=['chartkick.ext.charts'])

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

class LastAccessQueue(object):
    def __init__(self, size = 30):
        self.queue = [None for i in xrange(size)]

    def nonull_queue(self):
        return reversed(filter(lambda x: not x is None, self.queue))

    def add(self, distance):
        if not distance.meta2.video_id in [item["id"] for item in self.nonull_queue()]:
            self.queue.append({
                "id": distance.meta2.video_id,
                "title": distance.meta2.title,
                "distance": distance.distance,
                "thumbnail_url": distance.meta2.thumbnail_url
            })
            self.queue.pop(0)
video_queue = LastAccessQueue()

for video_id in smids:
    distance = pyon_service.distance(video_id)
    video_queue.add(distance)
print "ready"

@app.route("/")
def top():
    return redirect(url_for('each_view', video_id="1397117847"))
    return render_template("top.html", video_id_queue=video_queue.nonull_queue())

@app.route("/distance")
def distance():
    video_id = request.args.get('video_id').encode("utf-8")
    print video_id
    # validation
    p = re.compile('[sm0-9]*')
    if not p.match(video_id):
        return None

    return redirect(url_for('each_view', video_id=video_id))

    # calc distance
    distance = pyon_service.distance(video_id)
    video_queue.add(distance)
    # if not video_id in video_id_queue:
    #     video_id_queue.append(video_id)
    #     video_id_queue.pop(0)
    return jsonify({
        "video_id": distance.meta2.video_id,
        "title": distance.meta2.title,
        "distance": distance.distance,
        "sampledif": distance.sampledif
    })

@app.route("/view/<video_id>")
def each_view(video_id):
    distance = pyon_service.distance(video_id)
    video_queue.add(distance)
    return render_template(
        "each_view.html",
        video_id=video_id,
        title=distance.meta2.title,
        power=distance.distance,
        sample_diffs=distance.sampledif,
        chartdata=[[
                       chr(ord("A")+i),
                       diff["otherval"]-diff["thisval"]] for i,diff in enumerate(distance.sampledif)],
        video_id_queue=video_queue.nonull_queue(),
        description=VIDEO_DESCRIPTION
    )

if __name__ == "__main__":
    debug = (not os.environ.get("DEBUG") is None)
    print debug
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=debug, host="0.0.0.0", port=port)
