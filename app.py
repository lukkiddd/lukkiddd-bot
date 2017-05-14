# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
import re
import time
from flask import Flask, request, render_template, jsonify
import random
import urllib
from firebase import Firebase
import datetime


# -> Private Library
import skypy from skypy
import airbnbpy from airbnbpy


app = Flask(__name__, static_url_path='')

@app.route('/api/v1/', methods=["GET"])
def api_function():
	return None


if __name__ == '__main__':
    app.run(debug=True)