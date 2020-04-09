from flask import Flask, render_template
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
    return {
        'api': 'coffreMagic',
        'version': '0.0.1'
    }


@app.route('/api/coffre', methods=['GET', 'POST'])
def apiCoffreAll():
    value = bdd.hgetall('coffre')
    return {
        'value': str(value)
    }