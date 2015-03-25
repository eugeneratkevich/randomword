#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import db
import random
import csv

htmlsource = "<!DOCTYPE html><html><head><title>Translate</title><style>a{text-decoration:none;color:#000;}</style></head><body>%(body)s</body></html>"

class MainHandler(webapp2.RequestHandler):
    def get(self):

        output = ''
        oWordsCount = Words.all().count()
        number = random.randint(1, oWordsCount)
        q = db.GqlQuery("SELECT * FROM Words " +
                "WHERE number = :number " +
                "ORDER BY eng DESC", number = number)
        oWordsList = q.run(limit=1)
        #'Hello world!\n' + str(q.count()) + '\n' + output

        for contact in oWordsList:
            output += '\n<a href="/" align="center"><h1>%s<h1>\n<h3>%s</h3></a>\n' % (contact.eng, contact.rus)

        htmloutput = htmlsource % {'body': output}
        self.response.write(htmloutput)


class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        _getWordsList()
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/update', UpdateHandler),
], debug=True)



class Words(db.Model):
    number = db.IntegerProperty(required=True)
    eng = db.StringProperty(required=True)
    rus = db.StringProperty(required=True)

def _getWordsList():
    with open('words.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')

        query = Words.all(keys_only=True)
        entries =query.fetch(1000)
        db.delete(entries)
        counter = 0;

        for row in reader:
            print row
            try:
                counter = counter + 1
                eng =  u'%s' % row[0]
                rus =  u'%s' % row[1].decode('utf-8')
                c = Words(number = counter, eng=eng, rus=rus)
                c.put()

            except db.Error:
                print db.Error.message