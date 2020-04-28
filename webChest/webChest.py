from flask import Flask, render_template, jsonify
import redis
from webChest.config import config

app = Flask(__name__)
bdd = redis.Redis(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_PWD)

# Homepage
@app.route('/')
def homepage():
    return render_template('index.html')


# API
# TODO:
# * Do I need lock here ?

@app.route('/api')
def apiRoot():
    return jsonify({
        'api': 'coffreMagic',
        'version': '0.0.1'
    })


@app.route('/api/coffre', methods=['GET', 'POST'])
def apiCoffreAll():
    value = bdd.hgetall('coffre')
    converted = {}
    for key, val in value.items():
        converted[key.decode('utf-8')] = val.decode('utf-8')
    converted['positions'] = []
    value = bdd.lrange('coffrePosition', 0, -1)
    for pos in value:
        converted['positions'].append(pos.decode('utf-8'))
    return jsonify(converted)


@app.route('/api/config', methods=['GET', 'POST'])
def apiCoffreConfig():
    value = bdd.hgetall('coffreConfig')
    converted = {}
    for key, val in value.items():
        converted[key.decode('utf-8')] = val.decode('utf-8')
    value = bdd.hgetall('coffreElements')
    convertedBis = {}
    for key, val in value.items():
        convertedBis[key.decode('utf-8')] = val.decode('utf-8')
    converted['elements'] = convertedBis
    return jsonify(converted)