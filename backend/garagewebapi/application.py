"""
application.py
- creates a Flask app instance and registers the database object
"""
import logging
from flask import Flask
from flask_cors import CORS

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(32, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(36, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)


#Set up logger to console
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-6s %(levelname)-8s %(message)s')

def create_app(app_name='GARAGEWEB_API'):
  app = Flask(app_name)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  from garagewebapi.api import api
  app.register_blueprint(api, url_prefix="/api")

  return app