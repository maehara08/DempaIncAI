#!/usr/bin/env python

import json
from flask import Flask, Response
from flask import render_template
from flask import request, jsonify
from werkzeug import utils
import uuid
import sys, os
import logs

web_dir = os.path.dirname(os.path.abspath(__file__))
face_detect_dir = web_dir + '/../FaceDetect'
deeplearning_dir = web_dir + '/../DeepLearning'
sys.path.append(face_detect_dir)
sys.path.append(deeplearning_dir)
import detect
import dempa_eval

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    f = open('sample.json')
    json = f.read()
    f.close()
    return Response(response=json, status=200, mimetype="application/json")
    """
    f = request.files['file']
    filename = utils.secure_filename(f.filename)
    (fn, ext) = os.path.splitext(filename)
    input_path = '/tmp/' + uuid.uuid1().hex + ext
    print input_path
    f.save(input_path)

    faces = detect.detect_face_rotate(input_path, web_dir,'./static/out', out_dir='./static/out')
    print faces

    # res = dempa_eval.execute(faces, web_dir, deeplearning_dir + '/data/model.ckpt-13000_85per_input56_conv3_fc2')
    res = dempa_eval.execute(faces, web_dir, deeplearning_dir + '/tmp/data.2016-12-17/model.ckpt-10000')

    return jsonify({'results': res})

@app.route('/out', methods=['GET'])
def get_image():
    return 0

@app.route('/report', methods=['POST'])
def report():
    print request.form
    app.logger.info(",".join(['report', request.form["src"], request.form["correct_member_id"]]))
    return jsonify({'result': True})


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0')
