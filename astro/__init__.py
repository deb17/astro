import os

from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)

if 'DYNO' in os.environ: # only trigger SSLify if the app is running on Heroku
    sslify = SSLify(app)

from astro import routes
