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
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Index(webapp2.RequestHandler):
    def get(self):
        self.redirect("/blog")
    #base page, (redirect to blog to view recent posts)

class NewPost(webapp2.RequestHandler):
    def get(self): #use thin newpost template -
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)

    def post(self): #check and "create" post with a permalink
        title = self.request.get("title")
        post_body = self.request.get("post_body")

        if title and post_body:
            post = Posts(title=title, post_body=post_body) #uses database class to generate a new entry in DB with this title and post_body
            post.put() #adds to database
            perm = str(post.key().id())
            self.redirect("/blog/"+perm)
        else:
            error = "Whoops, you left something out"
            new = jinja_env.get_template("newpost.html")
            content = new.render(title=title, post_body = post_body, error=error) #passes any title and body entered along with applicable error message into newpost template
            self.response.write(content)

class Posts(db.Model):  #database of previous and newly added posts
    title = db.StringProperty(required=True)
    post_body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)

class RecentPosts(webapp2.RequestHandler):
    def get(self):
        query = Posts.all().order("-created") #query database to identify db entries in order of creation
        recent_posts = query.fetch(limit = 5) #assign the most recent 5 to the recent_posts variable

        t = jinja_env.get_template("frontpage.html") #get dat template
        content = t.render(post = recent_posts) #render, passing in this info
        self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id): #pulling with ID reference to database - use post template
        unique_post = Posts.get_by_id(int(id))
        t = jinja_env.get_template("post.html")
        content = t.render(post = unique_post)
        self.response.write(content)

app = webapp2.WSGIApplication([ #contains unique routing in LC101 directions as well as a corresponding handler for each class above
    ('/', Index),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
    ('/blog', RecentPosts),
    ('/newpost', NewPost)
], debug=True)
