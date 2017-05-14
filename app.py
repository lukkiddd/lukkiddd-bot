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

app = Flask(__name__, static_url_path='')

@app.route('/api/register', methods=['GET','POST'])
def register():
	f_name = request.args.get('first name')
	l_name = request.args.get('last name')
	gender = request.args.get('gender')
	local = request.args.get('local')
	profile_pic = request.args.get('profile pic url')
	messenger_user_id = request.args.get('messenger user id')
	users = Firebase('https://bott-a9c49.firebaseio.com/lukkiddd/users/')
	users.push({
		'first_name': f_name,
		'last_name': l_name,
		'gender': gender,
		'local': local,
		'profile_pic': profile_pic,
		'messenger_user_id': messenger_user_id
	})
	return ok, 200

@app.route('/api/seller/add_item', methods=['GET','POST'])
def seller_add_item():
	f_name = request.args.get('first name')
	item_name = request.args.get('item_name')
	item_image = request.args.get('item_image')
	item_price = request.args.get('item_price')
	messenger_user_id = request.args.get('messenger user id')
	new_item = {
		'owner': f_name,
		'owner_messenger_id': messenger_user_id,
		'item_name': item_name,
		'item_image': item_image,
		'item_price': item_price,
		'created_at':str(datetime.datetime.now())
	}
	item = Firebase('https://bott-a9c49.firebaseio.com/lukkiddd/items/')
	item.push(new_item)
	message = [
		{'text': u'เรียบร้อยแล้ว! เดี๋ยวถ้ามีคนสนใจ จะทักไปบอกนะคะ :D'}
	]
	return jsonify(message)

@app.route('/api/buyer/get_items', methods=['GET','POST'])
def buyer_get_item():
	items = Firebase('https://bott-a9c49.firebaseio.com/lukkiddd/items/').get()
	el = []
	if(items == None):
		return ok, 200
	for item_key in items:
		print item_key
		item = Firebase('https://bott-a9c49.firebaseio.com/lukkiddd/items/' + item_key).get()
		if(item and len(el) < 10):
			el.append(
				{
					"title": item["item_name"],
					"image_url": item["item_image"],
					"subtitle": u"โดย " + item["owner"],
					"buttons":[
						{
							"set_attributes": {
								"seller_messenger_id": item["owner_messenger_id"],
								"seller_item": item["item_name"],
								"seller_item_price": item["item_price"]
							},
							"type": "show_block",
							"block_name": "mgs_b2s",
							"title": "สนใจ"
						},
						{
							"type":"element_share"
						}
					]
				}
			)
	message = {
		"messages": [{
				"attachment":{
					"type":"template",
					"payload":{
						"template_type":"generic",
						"elements": el
					}
				}
		}]
	}
	return jsonify(message)

@app.route('/api/buyer/msg/send', methods=['GET','POST'])
def buyer_send_message():
	return ok, 200


if __name__ == '__main__':
    app.run(debug=True)