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
import jinja
import os
from google.appengine.txt import db

class Index(webapp2.RequestHandler):

    #base page, (redirect to blog to view recent posts)

class NewPost(webapp2.RequestHandler):
    def get(self): #use thin newpost template -

    def post(self): #check and "create" post with a permalink

class Posts(webapp2.RequestHandler):  #database of previous and newly added posts
    title = db.StringProperty(Required=True)
    post_body = db.TextProperty(Required=True)
    created = db.DateTimeProperty(auto_now_add = True)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id): #pulling with ID reference to database - use post template
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([ #contains unique routing in LC101 directions as well as a corresponding handler for each class above
    ('/', MainHandler)
], debug=True)
