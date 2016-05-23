#!/usr/bin/python
#encoding=utf-8
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask
from flask import jsonify,render_template,request,abort
import time
import json
import hashlib
import commands

app = Flask(__name__)
channel_name = 'cv_channel'


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/api', methods=['POST'])
def api():
    if not request.json or not 'primetext' in request.json:
        abort(400)
    text = request.json['primetext'].decode('utf-8')
    if '"' in text or '\'' in text: text = ''
    temp = float(request.json['temperature'])
    seed = int(request.json['seed'])
    model = request.json['model']
    if not os.path.exists(model): return ''
    length = int(request.json['samplelength'])
    length = min(length, 200)
    command = u'th sample.lua "%s" -seed %d -primetext "%s" -temperature %.4f -length %d -gpuid %d' % (model, seed, text, temp, length, -1 if model.endswith('_cpu.t7') else 0)
    status, output = commands.getstatusoutput(command)
    print command
    print output
    return jsonify({"output": output}), 200
    
@app.route('/models')
def models():
    return jsonify({"models": ['cv/' + _ for _ in os.listdir('cv/') if _.endswith('.t7')]}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9987, debug=False)
