import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import time

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Human(ndb.Model):
    tors = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
    major = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            human_query = Human.query()
            human_query = human_query.filter(Human.email == user.email())
            human_data = human_query.fetch()
            if human_data:
                self.redirect('/homepage')
            else:
                greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
                self.response.out.write('%s' % greeting)
                template = jinja_environment.get_template('templates/register.html')
                self.response.write(template.render())
        else:
            self.response.write('<a href="%s">Sign in or register</a>.' %
            users.create_login_url('/'))

    def post(self):
        user = users.get_current_user()
        human1 = Human(tors=self.request.get('tors'),name=self.request.get('name'), year=self.request.get('year'), school=self.request.get('school'), major=self.request.get('major'), email=user.email())
        human1.put()
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        self.redirect('/homepage')




class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        time.sleep(1)
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        if human_data[0].tors == "Tutor":
            info = {
          'university': human_data[0].school,
          'major' : human_data[0].major,
          'year' : human_data[0].year,
          'name' : human_data[0].name,
          }
            template = jinja_environment.get_template('templates/tutorhome.html')
            self.response.write(template.render(info))
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
            self.response.out.write('%s' % greeting)
        elif human_data[0].tors == "Student":
            info = {
          'name': human_data[0].name,
          }
            template = jinja_environment.get_template('templates/studenthome.html')
            self.response.write(template.render(info))
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
            self.response.out.write('%s' % greeting)

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        time.sleep(1)
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        info = {
            'school': human_data[0].school,
            'major' : human_data[0].major,
            'year' : human_data[0].year,
            'name' : human_data[0].name,
        }
        template = jinja_environment.get_template('templates/studentprofile.html')
        self.response.write(template.render(info))
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        self.response.out.write('%s' % greeting)

class ResultsHandler(webapp2.RequestHandler):
    def post(self):
        search=self.request.get('searchbox')
        human_query = Human.query()
        human_query = human_query.filter(Human.major == search)
        human_data = human_query.fetch()
        names_of_results = ""
        keys_of_results = []
        y=0
        for x in human_data:
            keys_of_results.append({"id":str(x.key.id()), "link":"/profileviewer?id="+str(x.key.id())})
            y=y+1
        for x in human_data:
            names_of_results=names_of_results+"<div>"+x.name+"</div>"
        template_values = {
        'results':keys_of_results,
        }
        template = jinja_environment.get_template('templates/results.html')
        self.response.write(template.render(template_values))

class ProfileViewerHandler(webapp2.RequestHandler):
    def get(self):
        user_id=self.request.get('id')
        tutor = {
        'tutor': Human.get_by_id(int(user_id))
        }
        template = jinja_environment.get_template('templates/tutorhomeview.html')
        self.response.write(template.render(tutor))

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/homepage', HomePageHandler),
  ('/profile',ProfileHandler),
  ('/results', ResultsHandler),
  ('/profileviewer', ProfileViewerHandler),
], debug=True)
