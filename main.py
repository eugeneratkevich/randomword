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
import random
import jinja2
import os
from models import Words, _updateVocabsList


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
        n = self.request.get('n')
        oWordsList = Words.getRandomWord(n)
        self.render('front.html', oWordsList = oWordsList)


class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        _updateVocabsList()
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/update', UpdateHandler),
], debug=True)

