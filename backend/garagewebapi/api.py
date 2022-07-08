import os
import json
import logging
import time
from datetime import datetime
from flask import Blueprint, request, jsonify

import RPi.GPIO as GPIO


api = Blueprint('api', __name__, static_folder='static')

@api.route('/doors', methods=['GET', 'POST'])
def doors():
        doorstatepins = ((16,18),(32,36))
        doorstates = [0,0]
        httpstatus = 200

        if request.method == 'POST':
                post_data = json.loads(json.dumps(request.get_json()))
                garagedoor = post_data.get('door')
                garagecode = post_data.get('garagecode')
                pin = 0
                
                if garagecode == int(os.environ.get('GARAGECODE', 12345678)):
                        if garagedoor == 1:
                                pin = 7
                        elif garagedoor == 2:
                                pin = 11

                        if pin == 7 or pin == 11:
                                GPIO.output(pin, GPIO.LOW)
                                time.sleep(1)
                                GPIO.output(pin, GPIO.HIGH)
                                time.sleep(2)
                        else:
                                httpstatus = 403
                else:
                        httpstatus = 401

        if request.method == 'GET' or request.method == 'POST':
                for index, door in enumerate(doorstatepins):
                        pin1, pin2 = door

                        logging.debug("index = " + str(index) + " pin1 = " + str(pin1) + " pin2 = " + str(pin2))
                        if GPIO.input(pin1) == GPIO.HIGH and GPIO.input(pin2) == GPIO.HIGH:
                                logging.info("Garage is Opening/Closing")
                                doorstates[index] = 0
                        elif GPIO.input(pin1) == GPIO.LOW and GPIO.input(pin2) == GPIO.HIGH:
                                logging.info("Garage is Closed")
                                doorstates[index] = 1
                        elif GPIO.input(pin1) == GPIO.HIGH and GPIO.input(pin2) == GPIO.LOW:
                                logging.info("Garage is Open")
                                doorstates[index] = 2

        res = jsonify({'doorstates': doorstates })
        res.status_code = httpstatus
        res.headers.add('Access-Control-Allow-Origin', '*')

        return res


@api.route('/log')
def logfile():
        return api.send_static_file('log.txt')


# sanity check route
@api.route('/health', methods=['GET'])
def ping_pong():
   return jsonify('Alive')
