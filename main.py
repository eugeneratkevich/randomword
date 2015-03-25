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
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import random
import csv
import jinja2
import os


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    """This is the main Handler class that has all the common functions."""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainHandler(Handler):
    def get(self):
        output = ''
        wordsCount = Words.all(keys_only=True).count()
        try:
            without_number = int(self.request.get('n'))
            if without_number > 1 and without_number*2 > wordsCount:
                number = random.randint(1, without_number - 1)
            else:
                number = random.randint(without_number + 1, wordsCount)
        except ValueError:
            number = random.randint(1, wordsCount)
        q = db.GqlQuery("SELECT * FROM Words " +
                "WHERE number = :number " +
                "ORDER BY eng DESC", number = number)
        oWordsList = q.run(limit=1)
        self.render('front.html', oWordsList = oWordsList)


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
        count = query.count()
        entries =query.fetch(count)
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
