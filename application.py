#!flask/bin/python
# -*- coding: utf8 -*-
# encoding=utf8 
from flask import Flask
import re
import os
import sys
import json
import time
from datetime import datetime
from pymongo import MongoClient
import pymongo
import requests
from flask import Flask, request, render_template, jsonify

reload(sys)  
sys.setdefaultencoding('utf8')

application = Flask(__name__)
# mongolab_uri = "mongodb://localhost:27017/test"
# client = MongoClient(mongolab_uri,
#                      connectTimeoutMS=10000,
#                      socketTimeoutMS=None)

mongolab_uri = "mongodb://heroku_nzqplc8l:kbbpgnt5nnevh8elegapko78v9@ds231961.mlab.com:31961/heroku_nzqplc8l" #os.environ["MONGODB_URI"]
client = MongoClient(mongolab_uri,
                     connectTimeoutMS=10000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
db = client.get_default_database()


@application.route("/", methods=["GET"])
def index():
    return "Hello, World!"
@application.route("/api/custom", methods=["POST"])
def addcustomefiled():
    data = request.get_json()
    messenger_id = data["messenger_id"]
    del data["messenger_id"]
    dt = db.user_messenger.update({"messenger_id":messenger_id},{"$set":data})
    return "sucess",200

@application.route("/api/handlemessage", methods=["POST"])
def handle_message():
    data = request.get_json()
    longtext = data["text"]
    messenger_id= data["messenger_id"]
    detectPhone(messenger_id,longtext)
    detectCode(messenger_id,longtext)
    detectUSD(messenger_id,longtext)
    detectDiscount(messenger_id,longtext)
    detectQuestion(messenger_id,longtext)
    detectColor(messenger_id,longtext)
    detectSize(messenger_id,longtext)
    return "sucess", 200


def detectPhone(messenger_id, longtext):
    companyNumber = ["0977484889", "023 999 899", "012223344", "023 6 868 868"]
    pattern = re.compile(
        r"0[0-9]{8,10}|0\d{2}\-\d{3}\-\d{3}\-\d{1}|0\d{2}\-\d{3}\-\d{3}|855\d{8,9}", re.IGNORECASE)
    match = pattern.findall(str(longtext))
    print(match)
    for l in match:
        if l in companyNumber:
            match.remove(l)
    print("final match again ---")
    print(match)
    if len(match) > 0:
        dt = {
            "date": str(time.time()),
            "phone": match
        }
        # db.messenger_report.insert(dt)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "phone":  dt  } })

# detectPhone("023 999 899 070757390 .wing 0977484889 071-333-372-8 truemoney 070-757-390 85512521010 emoney 855977484889 85570757390 271-333-372-8")


def detectCode(messenger_id,longtext):
    pattern = re.compile(r"\d{8}", re.IGNORECASE)
    match = pattern.findall(str(longtext))
    print(match)
    for l in match[:]:
        if l[:1] == "0":
            match.remove(l)
    print(match)
    if len(match) > 0:
        dt = {
            "date": str(time.time()),
            "code": match
        }
        # db.messenger_report.insert(dt)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "code":  dt  } })
# detectCode("99889900 01234567 012345678 0989899 81234567")


def detectUSD(messenger_id,longtext):
    pattern = re.compile(r"USD\s\d+\.\d+", re.IGNORECASE)
    match = pattern.findall(str(longtext))
    print(match)
    if len(match) > 0:
        dt = {
            "function": "detectUSD",
            "amounts": match
        }
        # db.messenger_report.insert(dt)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "amounts": dt } })


def detectDiscount(messenger_id,longtext):
    data = {
        "text": longtext,
        "date": datetime.now()
    }

    if("discount" in longtext):
        data["_id"] = str(time.time())
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "discount": data  } })
    if("ចុះបាន" in longtext):
        data["_id"] = str(time.time())
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "discount": data  } })
    if("ចុះខ្លះអត់" in longtext):
        data["_id"] = str(time.time())
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "discount": data  } })
    if("ចុះ" in longtext):
        data["_id"] = str(time.time())
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "discount": data  } })


def detectQuestion(messenger_id,longtext):
    dt = {
    	"_id":str(time.time()),
        "text": longtext,
        "date": datetime.now()
    }
    if("ប៉ុន្មាន" in longtext):
       # db.messenger_report.insert(dt)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "questions": dt  } })
    if("មានឬអត់" in longtext):
        # db.messenger_report.insert(dt)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "questions": longtext  } })
    if("អ្វីខ្លះ" in longtext):
        # db.messenger_report.insert(dt)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "questions": longtext  } })

    if("ដែរឬទេ" in longtext):
        # db.messenger_report.insert(dt)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "questions": longtext  } })


def detectColor(messenger_id,longtext):
    data = {
        "text": longtext,
        "date": datetime.now()
    }
    if("color" in longtext):
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "color": data  } })
    if("ពណ៏" in longtext):
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "color": data  } })
    if("ព័ណ" in longtext):
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "color": data  } })


def detectSize(messenger_id,longtext):
    data = {
        "function": "detectSize",
        "text": longtext,
        "date": datetime.now()
    }
    if("size" in longtext):
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "size": longtext  } })
    if("ទំហំ" in longtext):
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "size": longtext  } })
    if("លេខ" in longtext):
        # db.messenger_report.insert(data)
        db.users_messenger.update({ "messenger_id": messenger_id },{ "$push": { "size": longtext  } })


if __name__ == "__main__":
    application.run(debug=True)
