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
  message = [
    {'text': u'ยินดีต้อนรับนะคะ'}
  ]
  return jsonify(message)

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
          "title": item["item_name"] + item["item_price"] + u" บาท",
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

@app.route('/api/chat/msg/send', methods=['GET','POST'])
def chatroom():
  sender_id = request.args.get("messenger user id")
  sender_name = request.args.get("first name")
  reciever_id = request.args.get("seller_messenger_id")
  msg = request.args.get("msg")
  send_message(sender_id,sender_name, reciever_id, msg)
  return ok, 200


def send_message(sender_id, sender_name, reciever, msg):
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "seller_messenger_id": sender_id,
        "sender": sender_name,
        "msg": msg
    })
    r = requests.post("https://api.chatfuel.com/bots/58ccfcdde4b02491f5311c13/users/"+ reciever +"/send?chatfuel_token=mELtlMAHYqR0BvgEiMq8zVek3uYUK3OJMbtyrdNPTrQB9ndV0fM7lWTFZbM4MZvD&chatfuel_block_id=5918677ce4b04ca345cf2d68", headers=headers, data=data)
    print r

@app.route('/api/chat/msg/notify', methods=['GET','POST'])
def chatroom_notify():
  sender_id = request.args.get("messenger user id")
  sender_name = request.args.get("first name")
  reciever_id = request.args.get("seller_messenger_id")
  item_name = request.args.get("item_name")
  headers = {
      "Content-Type": "application/json"
  }
  data = json.dumps({
      "buyer_id": sender_id,
      "sender": sender_name,
      "chat_item_name": item_name
  })
  r = requests.post("https://api.chatfuel.com/bots/58ccfcdde4b02491f5311c13/users/"+ reciever_id +"/send?chatfuel_token=mELtlMAHYqR0BvgEiMq8zVek3uYUK3OJMbtyrdNPTrQB9ndV0fM7lWTFZbM4MZvD&chatfuel_block_id=59186b42e4b04ca345dad411", headers=headers, data=data)
  return ok, 200

@app.route('/api/broadcast', methods=['GET','POST'])
def broadcast():
  sender_id = request.args.get("messenger user id")
  sender_name = request.args.get("first name")
  broadcast_item = request.args.get("broadcast_item")
  users = Firebase('https://bott-a9c49.firebaseio.com/lukkiddd/users/').get()
  headers = {
      "Content-Type": "application/json"
  }
  data = json.dumps({
      "seller_messenger_id": sender_id,
      "sender": sender_name,
      "broadcast_item": broadcast_item
  })
  for user_key in users:
    user_id = Firebase('https://bott-a9c49.firebaseio.com/lukkiddd/users/' + user_key + '/messenger_user_id').get()
    if(user_id != sender_id):
      if("https://scontent" in broadcast_item):
        r = requests.post("https://api.chatfuel.com/bots/58ccfcdde4b02491f5311c13/users/"+ user_id +"/send?chatfuel_token=mELtlMAHYqR0BvgEiMq8zVek3uYUK3OJMbtyrdNPTrQB9ndV0fM7lWTFZbM4MZvD&chatfuel_block_id=59187f88e4b04ca3461dbb0a", headers=headers, data=data)
      else:
        r = requests.post("https://api.chatfuel.com/bots/58ccfcdde4b02491f5311c13/users/"+ user_id +"/send?chatfuel_token=mELtlMAHYqR0BvgEiMq8zVek3uYUK3OJMbtyrdNPTrQB9ndV0fM7lWTFZbM4MZvD&chatfuel_block_id=5918735ce4b04ca345f5a19e", headers=headers, data=data)

@app.route('/api/broadcaster/chat/msg/notify', methods=['GET','POST'])
def broadcast_notify():
  sender_id = request.args.get("messenger user id")
  sender_name = request.args.get("first name")
  reciever_id = request.args.get("seller_messenger_id")
  item_name = request.args.get("broadcast_item")
  headers = {
      "Content-Type": "application/json"
  }
  data = json.dumps({
      "buyer_id": sender_id,
      "sender": sender_name,
      "chat_item_name": item_name
  })
  r = requests.post("https://api.chatfuel.com/bots/58ccfcdde4b02491f5311c13/users/"+ reciever_id +"/send?chatfuel_token=mELtlMAHYqR0BvgEiMq8zVek3uYUK3OJMbtyrdNPTrQB9ndV0fM7lWTFZbM4MZvD&chatfuel_block_id=59186b42e4b04ca345dad411", headers=headers, data=data)
  return ok, 200

if __name__ == '__main__':
    app.run(debug=True)