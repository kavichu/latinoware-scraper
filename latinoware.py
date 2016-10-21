import json
import re
import os
from lxml import html
import requests

from flask import Flask
from flask import request, jsonify

from mongo import Collections

import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

db = Collections()
app = Flask(__name__)

@app.route('/scraper', methods=['GET'])
def scraper():
  if db.keynotes.count() == 0 or db.speakers.count() == 0:
    page = requests.get('http://latinoware.org/palestrantes-2016/')
    tree = html.fromstring(page.content)

    keynotes = tree.xpath('//*[@id="lcp_instance_0"]/li')

    for e in keynotes:
      speaker = {
        "name": e.xpath('a[1]/text()')[0],
        "bio": e.xpath('p/text()')[0]
      }
      speaker_id = db.speakers.insert(speaker)
      db.keynotes.insert({"speaker_id": speaker_id})

    speakers = tree.xpath('//ul[contains(@class, "speaker")]')
    for er in speakers:
      for e in er.xpath('li'):
        speaker = {
          "name": e.xpath('h4/a/text()')[0],
          "bio": e.xpath('div/text()')[0] 
        }
        speaker_id = db.speakers.insert(speaker)

  cursor = db.keynotes.find()
  keynotes = [JSONEncoder().encode(e) for e in cursor]
  cursor = db.speakers.find()
  speakers = [JSONEncoder().encode(e) for e in cursor]

  response = {
    "keynotes": keynotes,
    "speakers": speakers,
    "hostname": os.environ["HOSTNAME"]
  }
  return jsonify(response) 

@app.route('/speakers', methods=['GET'])
def speakers():
  cursor = db.speakers.find()
  speakers = [JSONEncoder().encode(e) for e in cursor]

  response = {
    "speakers": speakers,
    "hostname": os.environ["HOSTNAME"]
  }
  return jsonify(response) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")